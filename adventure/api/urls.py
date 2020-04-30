############################################################

from django.urls import path

from adventure.api import views as api_views

############################################################

app_name = "adventure_api"

urlpatterns = [
    path(
        "start/",
        api_views.start,
    ),
    path(
        "move/",
        api_views.move,
    ),
    path(
        "speak/",
        api_views.speak,
    ),
]
