from django.urls import path

from onetime.entrypoints.web.onetimesecrets import views

urlpatterns = [
    path("", views.index, name="index"),
]
