from django.db.models.signals import post_save
from django.dispatch import receiver

from board.models import Board, Nodes


@receiver(post_save, sender=Board)
def game_flow(instance, created, **kwargs):
    if created:
        Nodes.objects.create(board=instance, next_player=instance.player_circle)
    else:
        # Get associated node.
        node = Nodes.objects.get(board=instance)
        # sets up the next turn if the game is unfinished
        if instance.status == 1:
            if node.next_player == instance.player_circle:
                node.next_player = instance.player_cross
            elif node.next_player == instance.player_cross:
                node.next_player = instance.player_circle
        else:
            node.next_player = None

        node.save()
