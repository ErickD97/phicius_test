import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from board.models import Board
from utils.test_methods import bulk_create_test_instances, create_test_instance

User = get_user_model()


class BoardModelTests(TestCase):
    """Tests for 'board.Board' model class."""

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="Erick", password="abc*.123")
        cls.user2 = User.objects.create_user(username="Erick1", password="abc*.123")

    def test_player_circle_field(self):
        """
        Test to check this is a required field and a Board object gets deleted upon deletion of it's related circle user
        player.
        """
        values = {
            "player_cross": self.user2,
        }
        instance, errors = create_test_instance(values=values, model=Board)
        self.assertIsNone(instance)
        values.update({"player_circle": self.user1})
        instance, errors = create_test_instance(values=values, model=Board)

        self.assertIsInstance(instance, Board)
        # Use case when players are the same user is not being tested because the user can't select himself in the
        # CreateBoardForm.

    def test_player_cross_field(self):
        """
        Test to check this is a required field and a Board object gets deleted upon deletion of it's related cross user
        player.
        """
        values = {
            "player_circle": self.user1,
        }
        instance, errors = create_test_instance(values=values, model=Board)
        self.assertIsNone(instance)
        values.update({"player_cross": self.user2})
        instance, errors = create_test_instance(values=values, model=Board)
        self.assertIsInstance(instance, Board)
        # Use case when players are the same user is not being tested because the user can't select himself in the
        # CreateBoardForm.

    def test_created_at_field(self):
        """Test to check this is not a required field and it gets automatically populated upon creation."""
        values = {"player_circle": self.user1, "player_cross": self.user2}
        instance, errors = create_test_instance(values=values, model=Board)
        self.assertIsInstance(instance, Board)
        self.assertTrue(instance.created_at is not None)
        self.assertIsInstance(instance.created_at, datetime.datetime)
        # check created_at datatype

    def test_positions_circle_field(self):
        """Test to check this is not a required field, it has a defined default value and a specific structure."""
        values = {"player_circle": self.user1, "player_cross": self.user2}
        default_value = {
            "A": [],
            "B": [],
            "C": [],
        }
        instance, errors = create_test_instance(values=values, model=Board)
        self.assertIsInstance(instance, Board)
        self.assertEqual(instance.positions_circle, default_value)
        # Integity of this data like row numbers over 3 or under 1 is not tested because a user has no way of
        # introducing these values.

    def test_positions_cross_field(self):
        """Test to check this is not a required field, it has a defined default value and a specific structure."""
        values = {"player_circle": self.user1, "player_cross": self.user2}
        default_value = {
            "A": [],
            "B": [],
            "C": [],
        }
        instance, errors = create_test_instance(values=values, model=Board)
        self.assertIsInstance(instance, Board)
        self.assertEqual(instance.positions_cross, default_value)
        # Integity of this data like row numbers over 3 or under 1 is not tested because a user has no way of
        # introducing these values.

    def test_status_field(self):
        """Test to check this is not a required field, it goes to 1 by default and has 4 options only."""
        values = {"player_circle": self.user1, "player_cross": self.user2}
        new_values = [
            [values, True],
            [{"status": 1}, True],
            [{"status": 2}, True],
            [{"status": 3}, True],
            [{"status": 4}, True],
            [{"status": 0}, False],
            [{"status": 5}, False],
        ]
        success, errors = bulk_create_test_instances(
            values=new_values, model=Board, has_constraints=True
        )
        instance, instance_errors = create_test_instance(values=values, model=Board)
        success.append(instance.status == 1)
        self.assertTrue(all(success))

    def test_get_absolute_url_method(self):
        """Test to check this method returs a correct value."""
        values = {"player_circle": self.user1, "player_cross": self.user2}
        instance, instance_errors = create_test_instance(values=values, model=Board)
        correct_url = reverse("board:board_play", kwargs={"pk": instance.pk})
        self.assertEqual(correct_url, instance.get_absolute_url())

    def test_ordering_meta_attribute(self):
        """Test to check 'board.Board' objects are ordered in descending order by creation date."""
        values = {"player_circle": self.user1, "player_cross": self.user2}
        new_values = [
            [values, True],
            [{"status": 1}, True],
            [{"status": 2}, True],
            [{"status": 3}, True],
            [{"status": 4}, True],
        ]
        success, errors = bulk_create_test_instances(values=new_values, model=Board)
        queryset1 = Board.objects.all()
        queryset2 = Board.objects.order_by("-created_at").all()
        self.assertQuerysetEqual(queryset1, queryset2)
