__all__ = (
    "KickException",
    "HTTPException",
    "Forbidden",
    "NotFound",
    "InternalKickException",
    "LoginFailure",
    "CloudflareBypassException",
)


class CloudflareBypassException(Exception):
    ...


class KickException(Exception):
    pass


class LoginFailure(KickException):
    pass


class HTTPException(KickException):
    def __init__(self, txt: str, status_code: int) -> None:
        super().__init__(txt)
        self.status_code = status_code


class Forbidden(HTTPException):
    def __init__(self) -> None:
        super().__init__("", 403)


class NotFound(HTTPException):
    def __init__(self, txt: str) -> None:
        super().__init__(txt, 404)


class InternalKickException(HTTPException):
    def __init__(self, txt: str) -> None:
        super().__init__(txt, 500)
