import django_tables2 as tables
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from board.models import Board


class BoardTable(tables.Table):

    class Meta:
        model = Board
        fields = ("player_circle", "player_cross", "status")

    def render_player_circle(self, value, record):
        return value.username

    def render_player_cross(self, value, record):
        return value.username

    def render_status(self, value, record):
        url = record.get_absolute_url()
        if value == "Unfinished":
            return format_html(f"<a href={url}>{_('Unfinished')}</a>")
        elif value == "Cross Victory":
            return format_html(f"<a href={url}>{_('Cross Victory')}</a>")
        elif value == "Circle Victory":
            return format_html(f"<a href={url}>{_('Circle Victory')}</a>")
        elif value == "Draw":
            return format_html(f"<a href={url}>{_('Draw')}</a>")

