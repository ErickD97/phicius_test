from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import reverse
from django.test import TestCase

from board.forms import CreateBoardForm
from board.models import Board

User = get_user_model()


class CreateBoardTests(TestCase):
    """ Tests for 'board:board_create' view. """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="Erick", password="abc*.123")
        cls.user2 = User.objects.create_user(username="Erick1", password="abc*.123")
        cls.user3 = User.objects.create_user(username="Erick2", password="abc*.123")
        cls.board = Board.objects.create(player_circle=cls.user1, player_cross=cls.user2)

        cls.url = reverse("board:board_create")

    def test_authentication_required(self):
        """ Test to check that only authenticated users can access this view. """
        success = []
        response = self.client.get(self.url)
        success.extend(
            [
                response.status_code == 302,
                response.url == f"{reverse('account_login')}?next={self.url}",
            ]
        )
        self.client.force_login(user=self.user1)
        response = self.client.get(self.url)
        success.extend(
            [
                response.status_code == 200,
                "board/board_form.html" in response.template_name,
            ]
        )
        self.assertTrue(all(success))

    def test_get_request(self):
        """ Test to check that correct parameters are sent over this type of requests. """
        success = []
        self.client.force_login(user=self.user1)
        response = self.client.get(self.url)
        choices = [self.user2, self.user3]
        form_choices = response.context_data["form"].fields["opponent"].queryset
        success.extend([
            response.status_code == 200,
            isinstance(response.context_data["form"], CreateBoardForm),
            all(item in form_choices for item in choices) and all(item in choices for item in form_choices),
        ])
        self.assertTrue(all(success))

    def test_post_requests(self):
        """ Test to check that proper actions are executed after a POST request. """
        self.board.delete()
        success = []
        self.client.force_login(user=self.user1)

        # Select circle
        data_dict = {
            "cross_or_circle": 1,
            "opponent": self.user2,
        }
        response = self.client.post(self.url, data=data_dict)
        success.extend([
            response.status_code == 302,
            Board.objects.filter(player_circle=self.user1, player_cross=self.user2, status=1).exists()
        ])

        # Select cross
        data_dict.update({"cross_or_circle": 2, "opponent": self.user3})
        response = self.client.post(self.url, data=data_dict)
        success.extend([
            response.status_code == 302,
            Board.objects.filter(player_circle=self.user3, player_cross=self.user1, status=1).exists()
        ])

        # Select invalid user
        data_dict.update({"cross_or_circle": 2, "opponent": self.user1})
        response = self.client.post(self.url, data=data_dict)
        success.extend([
            response.status_code == 200,
            response.context_data["form"].is_bound is True,
        ])

        # Select invalid team
        data_dict.update({"cross_or_circle": 5, "opponent": self.user2})
        response = self.client.post(self.url, data=data_dict)
        success.extend([
            response.status_code == 200,
            response.context_data["form"].is_bound is True,
        ])

        self.assertTrue(all(success))
