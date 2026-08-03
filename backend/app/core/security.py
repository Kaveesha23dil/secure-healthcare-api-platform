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
    issuer: str = ""
    audience: frozenset[str] = frozenset()

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
    return _validate_token(
        token=token,
        jwks_url=cfg.jwks_url,
        algorithms=cfg.jwt_algorithms,
        issuer=cfg.jwt_issuer,
        audience=cfg.jwt_audience,
        leeway=cfg.access_token_leeway_seconds,
        subject_claim="sub",
        role_claim="roles",
        scope_claim="scope",
    )


def validate_wso2_backend_token(token: str, settings: Settings | None = None) -> AuthenticatedUser:
    cfg = settings or get_settings()
    return _validate_token(
        token=token,
        jwks_url=cfg.wso2_backend_jwt_jwks_url,
        algorithms=cfg.wso2_backend_jwt_algorithms,
        issuer=cfg.wso2_backend_jwt_issuer,
        audience=cfg.wso2_backend_jwt_audience,
        leeway=cfg.wso2_backend_jwt_leeway_seconds,
        subject_claim=cfg.wso2_subject_claim,
        role_claim=cfg.wso2_role_claim,
        scope_claim=cfg.wso2_scope_claim,
    )


def _string_set(value: object, claim_name: str, *, split_whitespace: bool) -> frozenset[str]:
    if isinstance(value, str):
        values = value.split() if split_whitespace else [value.strip()]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        values = [item.strip() for item in value]
    else:
        raise TokenValidationError(f"{claim_name} claim has an invalid type")
    if any(not item for item in values):
        raise TokenValidationError(f"{claim_name} claim contains an empty value")
    return frozenset(values)


def _validate_token(
    *,
    token: str,
    jwks_url: str,
    algorithms: list[str],
    issuer: str,
    audience: str,
    leeway: int,
    subject_claim: str,
    role_claim: str,
    scope_claim: str,
) -> AuthenticatedUser:
    try:
        header = jwt.get_unverified_header(token)
        algorithm = header.get("alg")
        if (
            not isinstance(algorithm, str)
            or algorithm.lower() == "none"
            or algorithm not in algorithms
        ):
            raise TokenValidationError("Token algorithm is not allowed")
        signing_key = _jwks_client(jwks_url).get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=algorithms,
            issuer=issuer,
            audience=audience,
            leeway=leeway,
            options={"require": ["exp", "iss", "aud", subject_claim]},
        )
    except (jwt.PyJWTError, ValueError, OSError, TokenValidationError) as exc:
        raise TokenValidationError("Access token validation failed") from exc
    subject = payload.get(subject_claim)
    if not isinstance(subject, str) or not subject:
        raise TokenValidationError("Access token subject is invalid")
    roles = _string_set(payload.get(role_claim, []), role_claim, split_whitespace=False)
    scopes = _string_set(payload.get(scope_claim, []), scope_claim, split_whitespace=True)
    token_issuer = payload.get("iss")
    raw_audience = payload.get("aud")
    if not isinstance(token_issuer, str):
        raise TokenValidationError("Token issuer claim is invalid")
    audiences = _string_set(raw_audience, "aud", split_whitespace=False)
    return AuthenticatedUser(subject, roles, scopes, token_issuer, audiences)
