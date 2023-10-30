from django.contrib import admin

from board.models import Board, Nodes


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Nodes)
class NodesAdmin(admin.ModelAdmin):
    pass


# No much work into this, everything relevant for the game can be done as a regular user.
