from django.dispatch import receiver
from django.db.models.signals import post_save

from board.models import Board, Nodes


@receiver(post_save, sender=Board)
def game_flow(instance, created, **kwargs):
    if created:
        Nodes.objects.create(board=instance, next_player=instance.player_circle)
    else:
        # Get associated node.
        node = Nodes.objects.get(board=instance)
        # Sort positions in ascending order
        for item in ["A", "B", "C"]:
            instance.positions_circle[item] = instance.positions_circle[item].sort()
            instance.positions_cross[item] = instance.positions_cross[item].sort()
        # update status according to positions
        instance.status = check_game_status(instance)
        # sets up the next turn if the game is unfinished
        if instance.status == 1:
            if node.next_player == instance.player_circle:
                node.next_player = instance.player_cross
            elif node.next_player == instance.player_cross:
                node.next_player = instance.player_circle
        else:
            node.next_player = None

        instance.save()
        node.save()


def check_game_status(board):
    total_moves = 0
    status = board.status

    # Check for diagonal victory
    if (1 in board.positions_circle["A"] and 2 in board.positions_circle["B"] and 3 in board.positions_circle["C"]) or (3 in board.positions_circle["A"] and 2 in board.positions_circle["B"] and 1 in board.positions_circle["C"]):
        status = 3
    elif (1 in board.positions_cross["A"] and 2 in board.positions_cross["B"] and 3 in board.positions_cross["C"]) or (3 in board.positions_cross["A"] and 2 in board.positions_cross["B"] and 1 in board.positions_cross["C"]):
        status = 2

    if status != board.status:
        return status

    # Check for row victories

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

    # Check for column victories
    circle_column = set(board.positions_circle["A"]).intersection(set(board.positions_circle["B"]), set(board.positions_circle["C"]))
    cross_column = set(board.positions_cross["A"]).intersection(set(board.positions_cross["B"]), set(board.positions_cross["C"]))

    if circle_column:
        status = 3
    elif cross_column:
        status = 2

    if status == board.status:
        if total_moves == 9:
            status = 4
    return status

