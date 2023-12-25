from typing import Any, Dict, Optional

from kira_client.stores.base_file_store import BaseFileStore


class RequestAction:
    def __init__(self, url: str, method: str):
        self.url = url
        self.method = method


class Action:
    def __init__(self, action_type: str, options: Any):
        self.action_type = action_type
        self.options = options


class Intent:
    def __init__(self, name: str, description: str, action: Optional[Action] = None):
        self.name = name
        self.description = description
        self.action = action


class IntentStore(BaseFileStore):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def get_all(self) -> list[Intent]:
        intents_data = self.read()
        return [self.__create_intent_from_dict(intent_dict) for intent_dict in intents_data]

    def get_intent_by_name(self, name: str) -> Optional[Intent]:
        intents = self.get_all()
        return next((intent for intent in intents if intent.name == name), None)

    def __create_intent_from_dict(self, intent_dict: Dict[str, Any]) -> Intent:
        action = self.__create_action_from_data(intent_dict.get("action"))
        return Intent(name=intent_dict["name"], description=intent_dict["description"], action=action)

    @staticmethod
    def __create_action_from_data(action_data: Optional[Dict[str, Any]]) -> Optional[Action]:
        if action_data is None:
            return None

        action_type = action_data["type"]
        options = action_data.get("options", {})

        match action_type:
            case "request":
                return Action(action_type, RequestAction(**options))

        return None
