from dependency_injector.wiring import Provide, inject
from django.shortcuts import render

from onetime.configurator.containers import Container
from onetime.entrypoints.web.onetimesecrets.forms import SecretForm
from onetime.use_cases.manager import SecretAndUrlManager


@inject
def index(
    request,
    secret_and_url_manager: SecretAndUrlManager = Provide[
        Container.secret_and_url_manager
    ],
):
    if request.method == "POST":
        form = SecretForm(request.POST)
        if form.is_valid():
            secret = form.cleaned_data["secret"]
            secret_and_url_manager.generate_secret_and_url(secret)
            # TODO: redirect to uuid link
    form = SecretForm()
    return render(request, "onetimesecrets/index.html", {"form": form})
