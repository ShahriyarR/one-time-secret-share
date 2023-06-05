from dependency_injector.wiring import Provide, inject
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from onetime.configurator.containers import Container
from onetime.entrypoints.web.onetimesecrets.forms import SecretCreateForm
from onetime.use_cases.exceptions import (
    SecretDataWasAlreadyConsumedException,
    URLExpiredException,
    UUIDNotFoundException,
)
from onetime.use_cases.manager import SecretAndUrlManager


@inject
def index(
    request,
    secret_and_url_manager: SecretAndUrlManager = Provide[
        Container.secret_and_url_manager
    ],
):
    if request.method == "POST":
        form = SecretCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["secret"]
            uuid = secret_and_url_manager.generate_secret_and_url(data)
            secret_url = request.build_absolute_uri(reverse("secret", args=(uuid,)))
            return render(
                request,
                "onetimesecrets/index.html",
                {"form": form, "secret_url": secret_url},
            )
    form = SecretCreateForm()
    return render(request, "onetimesecrets/index.html", {"form": form})


@inject
def secret(
    request,
    uuid: str,
    secret_and_url_manager: SecretAndUrlManager = Provide[
        Container.secret_and_url_manager
    ],
):
    if request.method == "POST":
        try:
            data = secret_and_url_manager.get_secret(uuid)
        except UUIDNotFoundException as e:
            return HttpResponseBadRequest(str(e))
        except SecretDataWasAlreadyConsumedException as e:
            return HttpResponseBadRequest(str(e))
        except URLExpiredException as e:
            return HttpResponseBadRequest(str(e))
        return render(request, "onetimesecrets/show_secret.html", {"secret_data": data})

    return render(request, "onetimesecrets/show_secret.html")
