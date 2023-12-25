from kira_client.stores.base_file_store import BaseFileStore


class Intent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class IntentStore(BaseFileStore):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def get_all(self) -> list[Intent]:
        intents_data = self.read()
        return [Intent(**intent_dict) for intent_dict in intents_data]
