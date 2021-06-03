from aiohttp import ClientResponse


class LibraryException(Exception):
    """Base Error that other errors inherit from."""

    pass


class NoInitialisedSession(LibraryException):
    """Raised when a ClientSession is not available. Created on __aenter__, or when passed."""

    pass


class HTTPException(LibraryException):
    """Raised when an HTTP Error occurs."""

    def __init__(self, *args, status_code: int):
        self.status_code = status_code

        super().__init__(*args)


class RatelimitException(HTTPException):
    """Raised when getting a 429 response from Google

    Parameters:
        resp_content: Response body    as str
        resp_headers: Response headers as dict
    """

    def __init__(self, *args, resp_content, resp_headers: dict):
        self.resp_content = resp_content
        self.resp_headers = resp_headers

        super().__init__(*args, status_code=429)


class AuthorizationException(HTTPException):
    """Raised when getting a 401 response from Google"""

    def __init__(self, *args):
        super().__init__(*args, status_code=401)


class UnknownResponse(HTTPException):
    """Raised when getting an unknown JSON response from Google

    Parameters:
        resp: The unrecognisable JSON response decoded into a dictionary.
    """

    def __init__(self, *args, resp: ClientResponse):
        self.resp = resp

        super().__init__(*args, status_code=200)


__all__ = [
    "LibraryException", "NoInitialisedSession", "HTTPException", "RatelimitException", "AuthorizationException",
    "UnknownResponse"
]
