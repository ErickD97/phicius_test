from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from board import constants
from utils.messages import MESSAGES


class Board(models.Model):

    player_cross = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Player Cross"),
        on_delete=models.CASCADE
    )
    player_circle = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Player Circle"),
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    positions_cross = models.JSONField(
        verbose_name=_("Positions played by cross"),
        default={"A": [], "B": [], "C": []}
    )
    positions_circle = models.JSONField(
        verbose_name=_("Positions played by circle"),
        default={"A": [], "B": [], "C": []}
    )

    status = models.IntegerField(
        verbose_name=_("Game Status"),
        choices=constants.STATUS,
        default=1
    )

    def clean(self):
        super().clean()
        if self.player_cross == self.player_circle:
            raise ValidationError(MESSAGES["SYS001"].value)

        #TODO: Validation for positions.
