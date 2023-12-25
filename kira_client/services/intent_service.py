from kira_client.services import HttpClient
from kira_client.stores import Intent, IntentStore, RequestAction


class IntentService:
    def __init__(self, http_client: HttpClient, intent_store: IntentStore):
        self.intent_store = intent_store
        self.http_client = http_client

    def get_all_intents(self) -> list[Intent]:
        return self.intent_store.get_all()

    def process_intent_action(self, intent_name: str):
        intent = self.intent_store.get_intent_by_name(intent_name)

        if intent is None or intent.action is None:
            return False

        match intent.action.action_type:
            case "request":
                self.__process_request_action(intent.action.options)

        return True

    def __process_request_action(self, options: RequestAction) -> bool:
        self.http_client.request(options.method, options.url)

        return True
