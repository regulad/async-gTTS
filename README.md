# asyncgTTS

Asynchronous interfaces to the [official Google Text to Speech](https://cloud.google.com/text-to-speech) API written with aiohttp.

[googleapis/python-texttospeech](https://github.com/googleapis/python-texttospeech/blob/3125b714f547191a830faecb5ae0b830e53e99fd/google/cloud/texttospeech_v1/services/text_to_speech/async_client.py#L35) is a much better version of this same idea, if you need it.

### Example

```python
import asyncio
import json

from asyncgTTS import AsyncGTTSSession


async def main():
    with open("SERVICE_ACCOUNT.JSON") as service_account_json:
        service_account_dict = json.load(service_account_json)

    async with AsyncGTTSSession.from_service_account(service_account_dict) as google_tts:
        audio_bytes = await google_tts.synthesize("Hello World")

    with open("Hello_world.mp3", "wb") as f:
        f.write(audio_bytes)


asyncio.run(main())
```
