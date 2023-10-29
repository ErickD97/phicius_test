from typing import List

from django.core.exceptions import ValidationError
from pydantic import BaseModel, Field, field_validator

from board.models import Board
from utils.messages import MESSAGES


class NewMoveStructure(BaseModel):
    board_id: list = List[str]
    position: list = List[str]

    @field_validator("board_id")
    def board_exists(cls, v, values, **kwargs):
        try:
            int(v[0])
        except ValueError:
            raise ValidationError(MESSAGES["SYS006"].value)
        exists = Board.objects.filter(id=int(v[0])).exists()
        if not exists:
            raise ValidationError(
                MESSAGES["SYS003"].value.format(f"{Board._meta.verbose_name.title()}")
            )
        return v

    @field_validator("position")
    def valid_position(cls, v, values, **kwargs):
        if values.data.get("board_id", None):
            board = Board.objects.get(id=values.data.get("board_id")[0])
            column, row = v[0].split("_")

            if column not in ["A", "B", "C"] or int(row) not in [1, 2, 3]:
                raise ValidationError(MESSAGES["SYS004"].value)

            if (
                int(row) in board.positions_circle[column]
                or int(row) in board.positions_cross[column]
            ):
                raise ValidationError(MESSAGES["SYS005"].value)

        return v
