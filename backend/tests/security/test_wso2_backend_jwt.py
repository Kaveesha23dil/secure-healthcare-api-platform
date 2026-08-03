from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.security import TokenValidationError, validate_wso2_backend_token


def wso2_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "app_env": "test",
        "auth_mode": "wso2_backend_jwt",
        "allow_direct_access": True,
        "wso2_backend_jwt_issuer": "https://wso2.example.invalid",
        "wso2_backend_jwt_audience": "secure-healthcare-api",
        "wso2_backend_jwt_jwks_url": "https://wso2.example.invalid/jwks",
        "wso2_backend_jwt_algorithms": ["RS256"],
        "wso2_backend_jwt_leeway_seconds": 0,
    }
    values.update(overrides)
    return Settings(**values)


def assertion(private_key: object, **overrides: object) -> str:
    payload: dict[str, object] = {
        "sub": "patient-a",
        "iss": "https://wso2.example.invalid",
        "aud": "secure-healthcare-api",
        "exp": datetime.now(UTC) + timedelta(minutes=2),
        "nbf": datetime.now(UTC) - timedelta(seconds=1),
        "roles": ["patient"],
        "scope": "doctor:read appointment:read",
    }
    payload.update(overrides)
    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "wso2-test"})


@pytest.fixture
def signing_key(monkeypatch):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    monkeypatch.setattr(
        "app.core.security._jwks_client",
        lambda _url: SimpleNamespace(
            get_signing_key_from_jwt=lambda _token: SimpleNamespace(key=public_key)
        ),
    )
    return private_key


def test_valid_claim_formats_create_immutable_context(signing_key) -> None:
    patient = validate_wso2_backend_token(assertion(signing_key), wso2_settings())
    doctor = validate_wso2_backend_token(
        assertion(signing_key, sub="doctor-a", roles="doctor", scope=["appointment:read"]),
        wso2_settings(),
    )
    administrator = validate_wso2_backend_token(
        assertion(signing_key, sub="admin-a", roles=["administrator"], scope="admin:manage"),
        wso2_settings(),
    )
    assert patient.roles == frozenset({"patient"})
    assert doctor.roles == frozenset({"doctor"})
    assert administrator.scopes == frozenset({"admin:manage"})
    assert patient.issuer == "https://wso2.example.invalid"
    assert patient.audience == frozenset({"secure-healthcare-api"})


def test_invalid_wso2_claims_fail_closed(signing_key) -> None:
    invalid_tokens = (
        assertion(signing_key, exp=datetime.now(UTC) - timedelta(seconds=1)),
        assertion(signing_key, iss="https://wrong.example.invalid"),
        assertion(signing_key, aud="wrong-audience"),
        assertion(signing_key, roles={"patient": True}),
        assertion(signing_key, scope={"doctor:read": True}),
        assertion(signing_key, sub=None),
    )
    for token in invalid_tokens:
        with pytest.raises(TokenValidationError):
            validate_wso2_backend_token(token, wso2_settings())


def test_unsupported_and_unsigned_algorithms_are_rejected(signing_key) -> None:
    unsupported = jwt.encode(
        {
            "sub": "patient-a",
            "iss": "https://wso2.example.invalid",
            "aud": "secure-healthcare-api",
            "exp": datetime.now(UTC) + timedelta(minutes=1),
        },
        key="local-test-only",
        algorithm="HS256",
    )
    unsigned = jwt.encode(
        {"sub": "patient-a", "exp": datetime.now(UTC) + timedelta(minutes=1)},
        key="",
        algorithm="none",
    )
    for token in (unsupported, unsigned):
        with pytest.raises(TokenValidationError):
            validate_wso2_backend_token(token, wso2_settings())


def test_missing_assertion_and_forged_identity_headers_do_not_grant_access(
    client: TestClient, signing_key, monkeypatch
) -> None:
    settings = wso2_settings()
    monkeypatch.setattr("app.api.dependencies.auth.get_settings", lambda: settings)
    assert client.get("/api/v1/doctors").status_code == 401
    headers = {
        "X-JWT-Assertion": assertion(signing_key),
        "X-User-ID": "administrator",
        "X-Patient-ID": "forged-patient",
        "X-Doctor-ID": "forged-doctor",
        "X-Role": "administrator",
        "X-Scopes": "admin:manage appointment:read:all",
    }
    assert client.get("/api/v1/doctors", headers=headers).status_code == 200
    assert client.get("/api/v1/admin/appointments", headers=headers).status_code == 403


def test_test_override_is_impossible_outside_test_environment() -> None:
    with pytest.raises(ValueError):
        Settings(app_env="production", auth_mode="test_override")
