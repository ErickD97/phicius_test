from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import reverse
from django.test import TestCase

from board.forms import CreateBoardForm
from board.models import Board

User = get_user_model()


class BoardPlayTests(TestCase):
    """ Tests for 'board:board_play' view. """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="Erick", password="abc*.123")
        cls.user2 = User.objects.create_user(username="Erick1", password="abc*.123")
        cls.user3 = User.objects.create_user(username="Erick2", password="abc*.123")
        cls.board = Board.objects.create(player_circle=cls.user1, player_cross=cls.user2)

        cls.url = reverse("board:board_play", kwargs={"pk": cls.board.pk})

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
                "board/board_detail.html" in response.template_name,
            ]
        )
        self.assertTrue(all(success))

    def test_get_request(self):
        """ Test to check that correct parameters are sent over this type of requests. """
        success =[]
        self.client.force_login(user=self.user1)
        response = self.client.get(self.url)
        success.extend(
            [
                response.status_code == 200,
                "board/board_detail.html" in response.template_name,
                response.context_data["board"] == self.board,
            ]
        )
        self.assertTrue(all(success))
