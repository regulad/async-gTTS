from base64 import b64decode
from typing import List
from urllib.parse import urlparse

from aiohttp import ClientSession, ClientResponse

from ._decos import require_session
from .errors import *
from .token import JSONWebTokenHandler

_GOOGLE_API_ENDPOINT = "https://texttospeech.googleapis.com/v1/"


class AsyncGTTSSession:
    """An interface with the Google Text-To-Speech API.

    A JSONWebTokenHandler must be passed, to provide headers to the ClientSession.

    A ClientSession can also be passed, which will be used to make requests. This is useful for connection pooling."""

    def __init__(
            self, json_web_token_handler: JSONWebTokenHandler,
            *, client_session: ClientSession = None, endpoint: str = _GOOGLE_API_ENDPOINT
    ):
        self._json_web_token_handler = json_web_token_handler
        self._endpoint = endpoint

        self.client_session = client_session
        self._client_session_is_passed = self.client_session is not None

    async def __aenter__(self):
        if not self._client_session_is_passed:
            self.client_session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._client_session_is_passed:
            await self.client_session.close()

    @classmethod
    def from_service_account(
            cls, service_account: dict, *, client_session: ClientSession = None, endpoint: str = _GOOGLE_API_ENDPOINT
    ):
        """Creates a new JSONWebTokenHandler from a SERVICE_ACCOUNT, and returns a class with it."""

        parsed_endpoint = urlparse(endpoint)
        audience = f"{parsed_endpoint.scheme}://{parsed_endpoint.netloc}/"

        json_web_token_handler = JSONWebTokenHandler(service_account, audience)

        return cls(json_web_token_handler, client_session=client_session, endpoint=endpoint)

    @property
    def _headers(self):
        return {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self._json_web_token_handler}",
        }

    def _process_resp(self, resp: ClientResponse) -> None:
        if resp.ok:
            return None
        elif resp.status == 401:
            raise AuthorizationException(resp.reason)
        elif resp.status == 429:
            raise RatelimitException(resp_content=resp.content, resp_headers=dict(resp.headers))
        else:
            raise HTTPException(resp.reason, status_code=resp.status)

    @require_session
    async def synthesize(
            self, text: str, *, language_code: str = "en", voice_name: str = "en-US-Wavenet-D", ret_type: str = "MP3"
    ) -> bytes:
        """Synthesizes text."""

        json_body = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": language_code,
                "name": voice_name,
            },
            "audioConfig": {
                "audioEncoding": ret_type
            }
        }

        async with self.client_session.post(f"{self._endpoint}text:synthesize", json=json_body, headers=self._headers) \
                as resp:
            resp = resp

            self._process_resp(resp)

            return_json: dict = await resp.json()

            try:
                return b64decode(return_json["audioContent"])
            except KeyError:
                raise UnknownResponse(resp=resp)

    @require_session
    async def get_voices(self, language_code: str = None) -> List[dict]:
        if language_code is not None:
            query_params = {"languageCode": language_code}
        else:
            query_params = {}

        async with self.client_session.get(f"{self._endpoint}voices", headers=self._headers, params=query_params) \
                as resp:
            resp = resp

            self._process_resp(resp)

            return_json: dict = await resp.json()

            try:
                return return_json["voices"]
            except KeyError:
                raise UnknownResponse(resp=resp)


__all__ = ["AsyncGTTSSession"]
