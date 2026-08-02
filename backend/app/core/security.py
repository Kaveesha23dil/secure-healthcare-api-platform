from dataclasses import dataclass
from functools import lru_cache

import jwt
from jwt import PyJWKClient

from app.core.config import Settings, get_settings


@dataclass(frozen=True)
class AuthenticatedUser:
    subject: str
    roles: frozenset[str]
    scopes: frozenset[str]

    @property
    def primary_role(self) -> str:
        return next(iter(sorted(self.roles)), "unknown")


class TokenValidationError(Exception):
    """Raised when a bearer token cannot be cryptographically validated."""


@lru_cache(maxsize=4)
def _jwks_client(url: str) -> PyJWKClient:
    return PyJWKClient(url, cache_keys=True, lifespan=300, timeout=5)


def validate_access_token(token: str, settings: Settings | None = None) -> AuthenticatedUser:
    cfg = settings or get_settings()
    try:
        header = jwt.get_unverified_header(token)
        algorithm = header.get("alg")
        if algorithm not in cfg.jwt_algorithms:
            raise TokenValidationError("Token algorithm is not allowed")
        signing_key = _jwks_client(cfg.jwks_url).get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=cfg.jwt_algorithms,
            issuer=cfg.jwt_issuer,
            audience=cfg.jwt_audience,
            leeway=cfg.access_token_leeway_seconds,
            options={"require": ["exp", "iss", "aud", "sub"]},
        )
    except (jwt.PyJWTError, ValueError, OSError, TokenValidationError) as exc:
        raise TokenValidationError("Access token validation failed") from exc
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise TokenValidationError("Access token subject is invalid")
    raw_roles = payload.get("roles", payload.get("role", []))
    if isinstance(raw_roles, str):
        raw_roles = [raw_roles]
    raw_scopes = payload.get("scope", payload.get("scp", ""))
    scopes = raw_scopes.split() if isinstance(raw_scopes, str) else raw_scopes
    return AuthenticatedUser(subject, frozenset(raw_roles or []), frozenset(scopes or []))
