import asyncio
from threading import Thread

from dependency_injector.wiring import inject, Provide
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from uvicorn import Config, Server

from kira_client.container import Container
from kira_client.controllers import TriggerController
from kira_client.routers import health_router, intent_router
from kira_client.services import ConfigService


@inject
def main(
    trigger_controller: TriggerController = Provide[Container.trigger_controller],
    logger_service=Provide[Container.logger_service],
):
    logger_service.info("Application started")
    trigger_controller.listen()


@inject
async def start_http_server(
    app: FastAPI,
    config_service: ConfigService = Depends(Provide[Container.config_service]),
):
    config = Config(app=app, host="0.0.0.0", port=config_service.HTTP_PORT, log_level="info")
    server = Server(config=config)

    await server.serve()


if __name__ == "__main__":
    load_dotenv()

    container = Container()
    container.init_resources()

    app = FastAPI()
    app.container = container
    app.include_router(intent_router)
    app.include_router(health_router)

    container.wire(modules=[__name__], packages=["kira_client.routers"])

    main_thread = Thread(target=main, args=())
    main_thread.start()

    asyncio.run(start_http_server(app))
