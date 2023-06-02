from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. One time secret share screen.")
