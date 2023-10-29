from django.urls import path
from board.views import (board_list, board_play, create_board)
from board.api import urls as api_urls

app_name = "board"
urlpatterns = [
    path("", board_list, name="board_list"),
    path("board/create", create_board, name="board_create"),
    path("board/<int:pk>/play", board_play, name="board_play"),
]

urlpatterns += api_urls.urlpatterns
