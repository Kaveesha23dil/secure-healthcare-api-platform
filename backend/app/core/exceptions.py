from dataclasses import dataclass


@dataclass
class ApiError(Exception):
    status_code: int
    title: str
    detail: str
    problem_type: str


class AuthenticationError(ApiError):
    def __init__(self, detail: str = "Valid authentication is required.") -> None:
        super().__init__(401, "Authentication required", detail, "authentication-required")


class AuthorizationError(ApiError):
    def __init__(self, detail: str = "The operation is not permitted.") -> None:
        super().__init__(403, "Forbidden", detail, "forbidden")


class ResourceNotFoundError(ApiError):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            404,
            f"{resource} not found",
            f"The requested {resource.lower()} does not exist or is not accessible.",
            f"{resource.lower().replace(' ', '-')}-not-found",
        )


class ConflictError(ApiError):
    def __init__(self, detail: str) -> None:
        super().__init__(409, "Conflict", detail, "conflict")


class BadRequestError(ApiError):
    def __init__(self, detail: str) -> None:
        super().__init__(400, "Bad request", detail, "bad-request")
