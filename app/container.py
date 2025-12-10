from dependency_injector import containers, providers
from app.db import get_db_sync
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app"])

    session = providers.Resource(
        get_db_sync,
    )