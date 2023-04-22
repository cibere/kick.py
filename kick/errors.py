class KickException(Exception):
    pass


class HTTPException(KickException):
    def __init__(self, txt: str) -> None:
        super().__init__(txt)


class Forbidden(HTTPException):
    pass


class NotFound(HTTPException):
    pass


class InternalKickException(HTTPException):
    pass
