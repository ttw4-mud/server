############################################################

from django.urls import path, include

############################################################

app_name = "api"

urlpatterns = [
    path(
        "accounts/",
        include("accounts.api.urls"),
    ),
    path(
        "adventure/",
        include("adventure.api.urls"),
    ),
]
