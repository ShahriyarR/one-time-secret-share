from onetime.configurator.containers import Container
from onetime.entrypoints.web.app import settings

container = Container()
container.config.from_dict(settings.__dict__)
