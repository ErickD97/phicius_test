import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from board.models import Board, Nodes
from utils.test_methods import create_test_instance, bulk_create_test_instances

User = get_user_model()


class NodesModelTests(TestCase):
    """ Tests for 'board.Nodes' model class. """
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="Erick", password="abc*.123")
        cls.user2 = User.objects.create_user(username="Erick1", password="abc*.123")
        cls.board = Board.objects.create(player_circle=cls.user1, player_cross=cls.user2)

    def test_board_field(self):
        """
        Test to check this is a required field, a Node object gets deleted upon deletion of it's related Board object,
        and a Nodes object is created upon creation of a Board object.
        """
        self.board.nodes.delete()

        values = [
            [{"next_player": self.user1}, False],
            [{"board": self.board}, True],
        ]
        success, errors = bulk_create_test_instances(values=values, model=Nodes, has_constraints=True)
        instance, instance_errors = create_test_instance(values={"board": self.board, "next_player": self.user1}, model=Nodes)
        self.assertIsInstance(instance, Nodes)
        self.board.delete()
        success.append(not Nodes.objects.filter(board_id=self.board.pk).exists())
        new_board = Board.objects.create(player_circle=self.user1, player_cross=self.user2)
        success.append(Nodes.objects.filter(board_id=new_board.pk).exists())
        self.assertTrue(all(success))

    def test_next_player_field(self):
        """
        Test to check this is a required field and a Nodes object gets deleted upon deletion of its related User
        object.
        """
        self.board.nodes.delete()

        values = {"board": self.board}
        instance, errors = create_test_instance(values=values, model=Nodes)
        self.assertIsNone(instance, Nodes)
        values.update({"next_player": self.user1})
        instance, errors = create_test_instance(values=values, model=Nodes)
        instance.next_player = self.user1
        instance.save()

        self.user1.delete()

        self.assertFalse(Nodes.objects.filter(next_player=self.user1).exists())
