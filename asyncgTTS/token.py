from time import time

import jwt

from .config import ServiceAccount


class JSONWebTokenHandler:
    """Handles bearer tokens from a service account."""

    def __init__(self, service_account: ServiceAccount, audience: str):
        self._service_account = service_account
        self._audience = audience

        self._issued_time = time()

    def __str__(self):
        return self.token

    @property
    def _headers(self) -> dict:
        return {"alg": "RS256", "typ": "JWT", "kid": self._service_account.private_key_id}

    @property
    def _payload(self) -> dict:
        """Returns payload to be encoded"""

        if time() > self._issued_time + 1200:
            self._issued_time = time()

        payload = {
            "aud": self._audience,
            "iss": self._service_account.client_email,
            "sub": self._service_account.client_email,
            "iat": self._issued_time,
            "exp": self._issued_time + 1200,
        }

        return payload

    @property
    def token(self) -> str:
        """Returns an encoded token."""

        return jwt.encode(
            payload=self._payload,
            key=self._service_account.private_key,
            algorithm="RS256",
            headers=self._headers,
        )


__all__ = ["JSONWebTokenHandler"]
