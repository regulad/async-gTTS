class LibraryException(Exception):
    """Base Error that other errors inherit from."""

    pass


class NoInitialisedSession(LibraryException):
    """Raised when a ClientSession is not available. Created on __aenter__, or when passed."""

    pass


class HTTPException(LibraryException):
    """Raised when an HTTP Error occurs."""

    def __init__(self, *args, status_code: int, **kwargs):
        self.status_code = status_code
        1
        super().__init__(*args, **kwargs)


class RatelimitException(HTTPException):
    """Raised when getting a 429 response from Google

    Parameters:
        resp_content: Response body    as str
        resp_headers: Response headers as dict
    """

    def __init__(self, *args, resp_content: str, resp_headers: dict, **kwargs):
        self.resp_content = resp_content
        self.resp_headers = resp_headers

        super().__init__(*args, status_code=429, **kwargs)


class AuthorizationException(HTTPException):
    """Raised when getting a 401 response from Google"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, status_code=401, **kwargs)


class UnknownResponse(LibraryException):
    """Raised when getting an unknown JSON response from Google

    Parameters:
        resp: The unrecognisable JSON response decoded into a dictionary.
    """

    def __init__(self, *args, resp: dict, **kwargs):
        self.resp = resp

        super().__init__(*args, **kwargs)
