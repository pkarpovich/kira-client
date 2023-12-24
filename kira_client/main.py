from dependency_injector.wiring import inject, Provide
from dotenv import load_dotenv

from kira_client.container import Container
from kira_client.controllers import TriggerController


@inject
def main(
    trigger_controller: TriggerController = Provide[Container.trigger_controller],
    logger_service=Provide[Container.logger_service],
):
    logger_service.info("Application started")
    trigger_controller.listen()


if __name__ == "__main__":
    load_dotenv()

    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
