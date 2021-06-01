from base64 import b64decode
from typing import List, Tuple

from aiohttp import ClientSession

from ._decos import require_session
from .errors import *
from .token import JSONWebTokenHandler


_GOOGLE_API_ENDPOINT = "https://texttospeech.googleapis.com/v1/"


class AsyncGTTS:
    """An interface with the Google Text-To-Speech API.

    A JSONWebTokenHandler must be passed, to provide headers to the ClientSession.

    A ClientSession can also be passed, which will be used to make requests."""

    def __init__(
            self, json_web_token_handler: JSONWebTokenHandler,
            *, client_session: ClientSession = None, endpoint: str = _GOOGLE_API_ENDPOINT
    ):
        self._json_web_token_handler = json_web_token_handler
        self._endpoint = endpoint

        self._client_session = client_session
        self._client_session_is_passed = self._client_session is not None

    async def __aenter__(self):
        if not self._client_session_is_passed:
            self._client_session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._client_session_is_passed:
            await self._client_session.close()

    @classmethod
    def from_service_account(cls, service_account: dict, *, endpoint: str = _GOOGLE_API_ENDPOINT):
        """Creates a new JSONWebTokenHandler from a SERVICE_ACCOUNT, and returns a class with it."""

        return cls(JSONWebTokenHandler(service_account), endpoint=_GOOGLE_API_ENDPOINT)

    @property
    def _headers(self):
        return {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self._json_web_token_handler}",
        }

    @require_session
    async def get(self, text: str, voice_lang: Tuple[str] = ("en-US-Standard-B", "en-us"),
                  ret_type: str = "OGG_OPUS") -> bytes:
        """Gets data from google."""

        json_body = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": voice_lang[-1],
                "name": voice_lang[0],
            },
            "audioConfig": {
                "audioEncoding": ret_type
            }
        }

        async with self._client_session.post(f"{self._endpoint}text:synthesize", json=json_body, headers=self._headers)\
                as resp:
            if resp.ok:
                resp_json = await resp.json()
                try:
                    audio_data = b64decode(resp_json["audioContent"])
                    return audio_data
                except KeyError:
                    raise UnknownResponse(resp=resp_json)
            elif resp.status == 401:
                raise AuthorizationException(resp.reason)
            elif resp.status == 429:
                raise RatelimitException(resp_content=resp.content, resp_headers=dict(resp.headers))
            else:
                raise HTTPException(resp.reason, status_code=resp.status)

    @require_session
    async def get_voices(self) -> List[dict]:
        async with self._client_session.get(f"{self._endpoint}voices", headers=self._headers) as resp:
            return (await resp.json())["voices"]
