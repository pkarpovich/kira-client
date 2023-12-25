from typing import get_type_hints, Union


class AppConfigError(Exception):
    pass


class ConfigService:
    OPENAI_API_KEY: str
    OPENAI_CHAT_MODEL: str = "gpt-4-1106-preview"
    OPENAI_SPEACH_RECOGNITION_MODEL: str = "whisper-1"

    PORCUPINE_ACCESS_KEY: str
    PORCUPINE_MODEL_PATH: str

    INTENT_STORE_PATH: str

    MICROPHONE_CHANNELS: int = 1
    MICROPHONE_RECORDING_DURATION: int = 7
    LED_STRIP_ENABLED: bool = False
    DEBUG: bool = False

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            var_type = get_type_hints(ConfigService)[field]
            try:
                if var_type == bool:
                    value = self._parse_bool(env.get(field, default_value))
                elif var_type == list[int]:
                    value = list(map(lambda item: int(item), self._parse_list(env.get(field, default_value))))
                elif var_type == list[str]:
                    value = self._parse_list(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                err_msg = 'Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                )

                raise AppConfigError(err_msg)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def _parse_bool(val: Union[str, bool]) -> bool:
        return val if type(val) == bool else val.lower() in ['true', 'yes', '1']

    @staticmethod
    def _parse_list(val: Union[str, list]) -> list:
        match val:
            case str():
                if ',' not in val:
                    return [val]

                return val.split(',')

            case _:
                return val
