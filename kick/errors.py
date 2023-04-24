__all__ = (
    "KickException",
    "HTTPException",
    "Forbidden",
    "NotFound",
    "InternalKickException",
)


class KickException(Exception):
    pass


class HTTPException(KickException):
    def __init__(self, txt: str) -> None:
        super().__init__(txt)


class Forbidden(HTTPException):
    def __init__(self) -> None:
        super().__init__("")


class NotFound(HTTPException):
    pass


class InternalKickException(HTTPException):
    pass
