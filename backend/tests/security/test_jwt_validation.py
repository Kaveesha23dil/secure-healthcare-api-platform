from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.config import Settings
from app.core.security import TokenValidationError, validate_access_token


def settings() -> Settings:
    return Settings(
        app_env="test",
        jwt_issuer="https://issuer.example.invalid",
        jwt_audience="secure-healthcare-api",
        jwks_url="https://issuer.example.invalid/jwks",
        jwt_algorithms=["RS256"],
        access_token_leeway_seconds=0,
    )


def token(private_key: object, **overrides: object) -> str:
    now = datetime.now(UTC)
    payload: dict[str, object] = {
        "sub": "patient-a",
        "iss": "https://issuer.example.invalid",
        "aud": "secure-healthcare-api",
        "exp": now + timedelta(minutes=5),
        "roles": ["patient"],
        "scope": "doctor:read appointment:read",
    }
    payload.update(overrides)
    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "test-key"})


def test_jwt_signature_issuer_audience_expiration_and_claims(monkeypatch) -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    monkeypatch.setattr(
        "app.core.security._jwks_client",
        lambda _url: SimpleNamespace(
            get_signing_key_from_jwt=lambda _token: SimpleNamespace(key=public_key)
        ),
    )
    actor = validate_access_token(token(private_key), settings())
    assert actor.subject == "patient-a"
    assert actor.roles == frozenset({"patient"})
    assert "appointment:read" in actor.scopes
    for invalid in (
        token(private_key, exp=datetime.now(UTC) - timedelta(seconds=1)),
        token(private_key, iss="https://wrong.example.invalid"),
        token(private_key, aud="wrong-audience"),
    ):
        with pytest.raises(TokenValidationError):
            validate_access_token(invalid, settings())


def test_invalid_signature_is_rejected(monkeypatch) -> None:
    signing_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    wrong_public_key = rsa.generate_private_key(public_exponent=65537, key_size=2048).public_key()
    monkeypatch.setattr(
        "app.core.security._jwks_client",
        lambda _url: SimpleNamespace(
            get_signing_key_from_jwt=lambda _token: SimpleNamespace(key=wrong_public_key)
        ),
    )
    with pytest.raises(TokenValidationError):
        validate_access_token(token(signing_key), settings())
