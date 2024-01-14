from dependency_injector.wiring import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

health_router = APIRouter(prefix="/health")


class HealthStatusResponse(BaseModel):
    status: str


@health_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthStatusResponse
)
@inject
def health_status() -> HealthStatusResponse:
    return HealthStatusResponse(status="ok")
