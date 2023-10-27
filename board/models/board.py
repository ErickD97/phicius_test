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
        on_delete=models.CASCADE,
        related_name="cross",
    )
    player_circle = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Player Circle"),
        on_delete=models.CASCADE,
        related_name="circle",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    positions_cross = models.JSONField(
        verbose_name=_("Positions played by cross"),
        default=constants.get_default_positions,
    )
    positions_circle = models.JSONField(
        verbose_name=_("Positions played by circle"),
        default=constants.get_default_positions,
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

    class Meta:
        ordering = ["-created_at"]

        # TODO: Validation for positions.
