############################################################

from django.urls import path, include

############################################################

app_name = "accounts_api"

urlpatterns = [
    path(
        "",
        include("rest_auth.urls"),
    ),
    path(
        "register/",
        include("rest_auth.registration.urls"),
    ),
]
