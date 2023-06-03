from django.apps import AppConfig

from onetime.entrypoints.web.app import container


class OnetimesecretsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "onetimesecrets"

    def ready(self):
        container.wire(modules=["onetime.entrypoints.web.onetimesecrets.views"])
