import django_filters
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from board.models import Board


class PlayerTypeFilter(django_filters.ChoiceFilter):
    field_name = "player_type"
    label = "Player Type"

    def filter(self, qs, value):
        if value == "cross":
            return qs.filter(player_cross=self.parent.request.user)
        elif value == "circle":
            return qs.filter(player_circle=self.parent.request.user)
        return qs

class VictoryFilter(django_filters.ChoiceFilter):
    field_name = "won"
    label = "Victory"
    def filter(self, qs, value):
        if value == "won":
            return qs.filter(Q(player_cross=self.parent.request.user, status=2) | Q(player_circle=self.parent.request.user, status=3))
        elif value == "loss":
            return qs.filter(Q(player_cross=self.parent.request.user, status=3) | Q(player_circle=self.parent.request.user, status=2))
        elif value == "draw":
            return qs.filter(Q(player_cross=self.parent.request.user, status=4) | Q(player_circle=self.parent.request.user, status=4))
        return qs

class BoardFilter(django_filters.FilterSet):
    player_type = PlayerTypeFilter(choices=[("cross", "Crosses"), ("circle", "Circles")])
    won = VictoryFilter(choices=[("won", "Victory"), ("loss", "Defeat"), ("draw", "Draw")])

    # @property
    # def qs(self, user_id=None):
    #     parent = super().qs
    #     return parent.filter(Q(player_cross=user_id) | Q(player_circle=user_id))

    class Meta:
        model = Board
        fields =    ("player_type", "won")
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }


