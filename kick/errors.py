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
    """
    This error is used when there is an error with the bypass script.
    """


class KickException(Exception):
    """
    This error is used when there is an error with kick.
    """


class LoginFailure(KickException):
    """
    This error is used when there is an error with logging in.
    """


class HTTPException(KickException):
    """
    This error is used when an error is ran into when making a request to kick.

    Attributes
    -----------
    status_code: int
        The HTTP code
    """

    def __init__(self, txt: str, status_code: int) -> None:
        super().__init__(txt)
        self.status_code = status_code


class Forbidden(HTTPException):
    """
    This error is used when kick returns a 403 status code.

    Attributes
    -----------
    status_code: int = 403
        The HTTP code
    """

    def __init__(self, txt: str = "") -> None:
        super().__init__(txt, 403)


class NotFound(HTTPException):
    """
    This error is used when kick returns a 404 status code.

    Attributes
    -----------
    status_code: int = 404
        The HTTP code
    """

    def __init__(self, txt: str) -> None:
        super().__init__(txt, 404)


class InternalKickException(HTTPException):
    """
    This error is used when kick returns a a 500 status code, or doesn't connect.

    Attributes
    -----------
    status_code: int = 500
        The HTTP code
    """

    def __init__(self, txt: str) -> None:
        super().__init__(txt, 500)
