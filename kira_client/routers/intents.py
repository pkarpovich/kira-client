from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from kira_client.container import Container
from kira_client.controllers import TriggerController

intent_router = APIRouter(prefix="/intents")


class RecognizeIntentResponse(BaseModel):
    ok: bool


@intent_router.post(
    "/start-recognition",
    status_code=status.HTTP_200_OK,
    response_model=RecognizeIntentResponse
)
@inject
def start_recognition(
    trigger_controller: TriggerController = Depends(Provide[Container.trigger_controller]),
) -> RecognizeIntentResponse:
    trigger_controller.pause_voice_trigger_detector()
    return RecognizeIntentResponse(ok=True)
