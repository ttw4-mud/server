############################################################

from django.urls import path

from adventure import api

############################################################

app_name = "adventure_api"

urlpatterns = [
    path(
        "start/",
        api.views.start,
    ),
    path(
        "move/",
        api.views.move,
    ),
    path(
        "speak/",
        api.views.speak,
    ),
]
