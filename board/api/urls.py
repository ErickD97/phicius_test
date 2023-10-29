from django.urls import path

from board.api.views import make_movement

urlpatterns = [path("move/", make_movement, name="make_movement")]
