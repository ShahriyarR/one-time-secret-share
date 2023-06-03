from django.shortcuts import render

from onetime.entrypoints.web.onetimesecrets.forms import SecretForm


def index(request):
    if request.method == "POST":
        form = SecretForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["secret"])
    form = SecretForm()
    return render(request, "onetimesecrets/index.html", {"form": form})
