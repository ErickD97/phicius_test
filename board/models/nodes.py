from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from board.models import Board


class Nodes(models.Model):

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    next_player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Next Player"),
        null=True,
    )
