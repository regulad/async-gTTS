from enum import Enum
from typing import List, Optional, Union


class Ssml(str):
    pass


class SynthesisInput:
    def __init__(self, synthesis_input: Union[Ssml, str]):
        self._synthesis_input = synthesis_input

    @property
    def synthesis_input(self):
        return self._synthesis_input

    def __dict__(self):
        if isinstance(self.synthesis_input, Ssml):
            field_name = "ssml"
        elif isinstance(self.synthesis_input, str):
            field_name = "text"

        return {
            field_name: self.synthesis_input
        }


class SsmlVoiceGender(Enum):
    SSML_VOICE_GENDER_UNSPECIFIED = "SSML_VOICE_GENDER_UNSPECIFIED"
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"


class VoiceSelectionParams:
    def __init__(
            self,
            language_code: str = "en-US",
            name: str = "en-US-Wavenet-D",
            *,
            ssml_gender: Optional[SsmlVoiceGender] = None,
    ):
        self._language_code = language_code
        self._name = name
        self._ssml_gender = ssml_gender

    @property
    def language_code(self):
        return self._language_code

    @property
    def name(self):
        return self._name

    @property
    def ssml_gender(self):
        return self._ssml_gender

    def __dict__(self):
        return {
            "languageCode": self.language_code,
            "name": self.name,
            "ssmlGender": self.ssml_gender,
        }


class AudioEncoding(Enum):
    AUDIO_ENCODING_UNSPECIFIED = "AUDIO_ENCODING_UNSPECIFIED"
    LINEAR16 = "LINEAR16"
    MP3 = "MP3"
    MP3_64_KBPS = "MP3_64_KBPS"
    OGG_OPUS = "OGG_OPUS"
    MULAW = "MULAW"
    ALAW = "ALAW"


class AudioConfig:
    def __init__(
            self,
            audio_encoding: AudioEncoding = AudioEncoding.MP3,
            *,
            speaking_rate: Optional[float] = None,
            pitch: Optional[float] = None,
            volume_gain_db: Optional[float] = None,
            sample_rate_hertz: Optional[int] = None,
            effects_profile_id: Optional[List[str]] = None,
    ):
        self._audio_encoding = audio_encoding
        self._speaking_rate = speaking_rate
        self._pitch = pitch
        self._volume_gain_db = volume_gain_db
        self._sample_rate_hertz = sample_rate_hertz
        self._effects_profile_id = effects_profile_id

    @property
    def audio_encoding(self):
        return self._audio_encoding

    @property
    def speaking_rate(self):
        return self._speaking_rate

    @property
    def pitch(self):
        return self._pitch

    @property
    def volume_gain_db(self):
        return self._volume_gain_db

    @property
    def sample_rate_hertz(self):
        return self._sample_rate_hertz

    @property
    def effects_profile_id(self):
        return self._effects_profile_id

    def __dict__(self):
        return {
            "audioEncoding": self.audio_encoding.value,
            "speakingRate": self.speaking_rate,
            "pitch": self.pitch,
            "volumeGainDb": self.volume_gain_db,
            "sampleRateHertz": self.sample_rate_hertz,
            "effectsProfileId": self.effects_profile_id,
        }


class TimepointType(Enum):
    TIMEPOINT_TYPE_UNSPECIFIED = "TIMEPOINT_TYPE_UNSPECIFIED"
    SSML_MARK = "SSML_MARK"


class TextSynthesizeRequestBody:
    def __init__(
            self,
            synthesis_input: SynthesisInput,
            *,
            voice_input: VoiceSelectionParams = VoiceSelectionParams(),
            audio_config_input: AudioConfig = AudioConfig(),
            enable_time_pointing_input: Optional[List[TimepointType]] = None,
    ):
        self._synthesis_input = synthesis_input
        self._voice_input = voice_input
        self._audio_config_input = audio_config_input
        self._enable_time_pointing_input = enable_time_pointing_input

    @property
    def synthesis_input(self):
        return self._synthesis_input

    @property
    def voice_input(self):
        return self._voice_input

    @property
    def audio_config_input(self):
        return self._audio_config_input

    @property
    def enable_time_pointing_input(self):
        return self._enable_time_pointing_input

    def __dict__(self):
        return {
            "input": self.synthesis_input.__dict__(),
            "voice": self.voice_input.__dict__(),
            "audioConfig": self.audio_config_input.__dict__(),
            "enableTimePointing": self.enable_time_pointing_input,
        }


class ServiceAccount:
    def __init__(
            self,
            type_input: str,
            project_id: str,
            private_key_id: str,
            private_key: str,
            client_email: str,
            client_id: str,
            auth_uri: str,
            token_uri: str,
            auth_provider_x509_cert_url: str,
            client_x509_cert_url: str,
    ):
        self._type_input = type_input
        self._project_id = project_id
        self._private_key_id = private_key_id
        self._private_key = private_key
        self._client_email = client_email
        self._client_id = client_id
        self._auth_uri = auth_uri
        self._token_uri = token_uri
        self._auth_provider_x509_cert_url = auth_provider_x509_cert_url
        self._client_x509_cert_url = client_x509_cert_url

    @property
    def type(self):
        return self._type_input

    @property
    def project_id(self):
        return self._project_id

    @property
    def private_key_id(self):
        return self._private_key_id

    @property
    def private_key(self):
        return self._private_key

    @property
    def client_email(self):
        return self._client_email

    @property
    def client_id(self):
        return self._client_id

    @property
    def auth_uri(self):
        return self._auth_uri

    @property
    def token_uri(self):
        return self._token_uri

    @property
    def auth_provider_x509_cert_url(self):
        return self._auth_provider_x509_cert_url

    @property
    def client_x509_cert_url(self):
        return self._client_x509_cert_url

    @classmethod
    def from_service_account_dict(cls, service_account_dict: dict):
        return cls(
            service_account_dict["type"],
            service_account_dict["project_id"],
            service_account_dict["private_key_id"],
            service_account_dict["private_key"],
            service_account_dict["client_email"],
            service_account_dict["client_id"],
            service_account_dict["auth_uri"],
            service_account_dict["token_uri"],
            service_account_dict["auth_provider_x509_cert_url"],
            service_account_dict["client_x509_cert_url"],
        )

    def __dict__(self):
        return {
            "type": self.type,
            "project_id": self.project_id,
            "private_key_id": self.private_key_id,
            "private_key": self.private_key,
            "client_email": self.client_email,
            "client_id": self.client_id,
            "auth_uri": self.auth_uri,
            "token_uri": self.token_uri,
            "auth_provider_x509_cert_url": self.auth_provider_x509_cert_url,
            "client_x509_cert_url": self.client_x509_cert_url,
        }

    def __getitem__(self, item):
        return self.__dict__()[item]


__all__ = [
    "Ssml", "SynthesisInput", "SsmlVoiceGender", "VoiceSelectionParams", "AudioEncoding", "AudioConfig",
    "TimepointType", "TextSynthesizeRequestBody", "ServiceAccount"
]
