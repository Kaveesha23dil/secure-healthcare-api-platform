from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import AuthenticatedUser, TokenValidationError, validate_access_token

OAUTH_SCOPES = {
    "doctor:read": "Read doctor directory information",
    "doctor:write": "Manage doctor records",
    "availability:read": "Read doctor availability",
    "availability:write": "Manage authorized availability",
    "appointment:create": "Create an appointment",
    "appointment:read": "Read owned or assigned appointments",
    "appointment:read:all": "Read appointments administratively",
    "appointment:update": "Update appointment states",
    "appointment:cancel": "Cancel an appointment",
    "patient:read": "Read patient summaries",
    "patient:write": "Manage patient accounts",
    "admin:manage": "Perform administrative functions",
}
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://localhost:9443/oauth2/authorize",
    tokenUrl="https://localhost:9443/oauth2/token",
    scopes=OAUTH_SCOPES,
    scheme_name="oauth2",
    auto_error=False,
)


def get_current_user(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> AuthenticatedUser:
    if token is None:
        raise AuthenticationError()
    try:
        user = validate_access_token(token)
    except TokenValidationError as exc:
        raise AuthenticationError() from exc
    request.state.actor_subject = user.subject
    request.state.actor_role = user.primary_role
    return user


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]


def require_scopes(*required: str) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    def dependency(user: CurrentUser) -> AuthenticatedUser:
        if not set(required).issubset(user.scopes):
            raise AuthorizationError()
        return user

    return dependency


def require_any_scope(*accepted: str) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    def dependency(user: CurrentUser) -> AuthenticatedUser:
        if not user.scopes.intersection(accepted):
            raise AuthorizationError()
        return user

    return dependency


def require_role(*roles: str) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    def dependency(user: CurrentUser) -> AuthenticatedUser:
        if not user.roles.intersection(roles):
            raise AuthorizationError()
        return user

    return dependency
