from pvporcupine import create


class VoiceTriggerDetector:
    def __init__(self):
        self.porcupine = create(
            access_key="",
            keywords=['Marcus'],
            model_path=""
        )

    def listen(self):
        pass
