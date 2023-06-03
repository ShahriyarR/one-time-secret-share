from django.urls import path

from onetime.entrypoints.web.onetimesecrets import views

urlpatterns = [
    path("secret/<str:uuid>", views.secret, name="secret"),
    path("", views.index, name="index"),
]
