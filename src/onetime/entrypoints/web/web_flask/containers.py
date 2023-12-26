from dependency_injector import containers, providers
from onetime.services.manager import SecretManager
from onetime.use_cases.manager import SecretAndUrlManager


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(modules=["onetime.entrypoints.web.web_flask.views"])

    secret_manager = providers.Factory(SecretManager)

    secret_and_url_manager = providers.Singleton(SecretAndUrlManager)
