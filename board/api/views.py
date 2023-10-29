from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from pydantic import ValidationError as PyValidationError
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from board.api.parameters.make_a_play import make_a_play_body, make_a_play_response_dict
from board.api.schemas import NewMoveStructure
from board.api.serializers import NewMoveStructureSerializer
from board.models import Board
from utils.messages import MESSAGES


class BoardGameplay(viewsets.GenericViewSet, APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = NewMoveStructureSerializer
    template_to_use = "board/board_list.html"

    @action(detail=False, methods=["post"])
    def make_a_play(self, request):
        errors = None
        message = None
        try:
            NewMoveStructure(**request.data)
            position = request.data.get("position")
            column, row = position.split("_")
            board_id = int(request.data.get("board_id"))
            assert bool(row) and bool(column), MESSAGES["SYS002"].value
        except (AssertionError, ValueError, ValidationError, PyValidationError) as ex:
            errors = ex
            messages.error(request, [str(error) for error in ex.args])
        try:
            with transaction.atomic():
                board = Board.objects.get(id=board_id)
                user = request.user
                if board.player_circle == user:
                    if isinstance(board.positions_circle[column], list):
                        board.positions_circle[column].append(int(row))
                    else:
                        board.positions_circle[column] = [int(row)]
                    positions_circle = board.positions_circle[column]
                    positions_circle.sort()
                else:
                    if isinstance(board.positions_cross[column], list):
                        board.positions_cross[column].append(int(row))
                    else:
                        board.positions_cross[column] = [int(row)]
                    positions_cross = board.positions_cross[column]
                    positions_cross.sort()
                board.status = check_game_status(board)
                board.save()
        except ObjectDoesNotExist as ex:
            errors = ex
            messages.error(request, [str(error) for error in ex.args])
        except Exception as ex:
            errors = ex
            messages.error(request, [str(error) for error in ex.args])
        if not errors:
            if board.status == 1:
                messages.success(
                    request, _("Great! Now wait for your opponent to play.")
                )
            elif board.status in [2, 3]:
                messages.success(request, _("Your victory!"))
            elif board.status == 4:
                messages.info(request, _("Draw!"))
        return HttpResponseRedirect(
            reverse("board:board_play", kwargs={"pk": board_id})
        )

    @swagger_auto_schema(
        method="post",
        operation_description=_("Make a move on the board."),
        request_body=make_a_play_body,
        responses=make_a_play_response_dict,
    )
    @action(detail=False, methods=["post"])
    def api_make_a_play(self, request):
        """ Just like the previous one, but intended to return Response objects for POSTMAN interactions and API
        documentation. """
        try:
            NewMoveStructure(**request.data)
            position = request.data.get("position")
            column, row = position.split("_")
            board_id = int(request.data.get("board_id"))
            assert bool(row) and bool(column), MESSAGES["SYS002"].value
        except (AssertionError, ValueError, ValidationError, PyValidationError) as ex:
            return Response(
                {"type": "PRECONDITION_FAILED", "errors": [str(error) for error in ex.args]},
                status=status.HTTP_412_PRECONDITION_FAILED,
            )
        try:
            with transaction.atomic():
                board = Board.objects.get(id=board_id)
                user = request.user
                if board.player_circle == user:
                    if isinstance(board.positions_circle[column], list):
                        board.positions_circle[column].append(int(row))
                    else:
                        board.positions_circle[column] = [int(row)]
                    positions_circle = board.positions_circle[column]
                    positions_circle.sort()
                else:
                    if isinstance(board.positions_cross[column], list):
                        board.positions_cross[column].append(int(row))
                    else:
                        board.positions_cross[column] = [int(row)]
                    positions_cross = board.positions_cross[column]
                    positions_cross.sort()
                board.status = check_game_status(board)
                board.save()
        except ObjectDoesNotExist as ex:
            return Response(
                {"type": "BAD_REQUEST", "errors": [str(error) for error in ex.args]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as ex:
            return Response(
                {"type": "BAD_REQUEST", "errors": [str(error) for error in ex.args]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if board.status == 1:
            message = _("Great! Now wait for your opponent to play.")
        elif board.status in [2, 3]:
            message = _("Your Victory!")
        else:
            message = _("Draw.")
        return Response(
            {"success": True, "message": message},
            headers=cache.no_cache,
            status=status.HTTP_200_OK,
        )


make_movement = BoardGameplay.as_view({"post": "make_a_play"})
api_make_movement = BoardGameplay.as_view({"post": "api_make_a_play"})


def check_game_status(board):
    total_moves = 0
    status = board.status

    # Check for diagonal victory
    if (
        1 in board.positions_circle["A"]
        and 2 in board.positions_circle["B"]
        and 3 in board.positions_circle["C"]
    ) or (
        3 in board.positions_circle["A"]
        and 2 in board.positions_circle["B"]
        and 1 in board.positions_circle["C"]
    ):
        status = 3
    elif (
        1 in board.positions_cross["A"]
        and 2 in board.positions_cross["B"]
        and 3 in board.positions_cross["C"]
    ) or (
        3 in board.positions_cross["A"]
        and 2 in board.positions_cross["B"]
        and 1 in board.positions_cross["C"]
    ):
        status = 2

    if status != board.status:
        return status

    # Check for column victories

    for key, values in board.positions_circle.items():
        total_moves += len(values)
        if values == [1, 2, 3]:
            status = 3

    for key, values in board.positions_cross.items():
        total_moves += len(values)
        if values == [1, 2, 3]:
            status = 2

    if status != board.status:
        return status

    # Check for row victories
    circle_column = set(board.positions_circle["A"]).intersection(
        set(board.positions_circle["B"]), set(board.positions_circle["C"])
    )
    cross_column = set(board.positions_cross["A"]).intersection(
        set(board.positions_cross["B"]), set(board.positions_cross["C"])
    )

    if circle_column:
        status = 3
    elif cross_column:
        status = 2

    if status == board.status:
        if total_moves == 9:
            status = 4
    return status
