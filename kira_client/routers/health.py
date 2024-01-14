from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from kira_client.container import Container
from kira_client.services import HardwareInfoService

health_router = APIRouter(prefix="/health")


class HealthStatusResponse(BaseModel):
    status: str
    cpu_temp: float


@health_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthStatusResponse
)
@inject
def health_status(
    hardware_info_service: HardwareInfoService = Depends(Provide[Container.hardware_info_service]),
) -> HealthStatusResponse:
    cpu_temp = hardware_info_service.get_cpu_temperature()

    return HealthStatusResponse(status="ok", cpu_temp=cpu_temp)
