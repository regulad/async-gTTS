import time

import jwt


class JSONWebTokenHandler:
    """Handles bearer tokens from a service account."""

    def __init__(
            self, service_account: dict,
    ):
        self._service_account = service_account

        self._expire_time = time.time() + 3600

    def __str__(self):
        return self._token

    @property
    def _token(self):
        """Returns an encoded token."""

        if time.time() >= self._expire_time:
            self._expire_time += 3600

        payload = {
            "aud": self._service_account["auth_uri"],
            "iss": self._service_account["client_email"],
            "sub": self._service_account["client_email"],
            "iat": int(time.time()),
            "exp": int(self._expire_time),
        }

        return jwt.encode(
            payload,
            self._service_account["private_key"],
            "RS256",
            {"kid": self._service_account["private_key"]},
        )
