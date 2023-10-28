from django.urls import path
from board.views import (board_list, create_board)

app_name = "board"
urlpatterns = [
    path("", board_list, name="index"),
    path("board/create", create_board, name="board_create"),
]
