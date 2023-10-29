from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import reverse
from django.test import TestCase

from board.filters import BoardFilter
from board.models import Board
from board.tables import BoardTable

User = get_user_model()


class BoardListTests(TestCase):
    """ Tests for 'board_list' view. """
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="Erick", password="abc*.123")
        cls.user2 = User.objects.create_user(username="Erick1", password="abc*.123")
        cls.user3 = User.objects.create_user(username="Erick2", password="abc*.123")
        cls.board = Board.objects.create(player_circle=cls.user1, player_cross=cls.user2)

        cls.url = reverse("board:board_list")

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
                "board/board_list.html" in response.template_name,
            ]
        )
        self.assertTrue(all(success))

    def test_get_request(self):
        """ Test to check parameters of the GET request, context data, templates and such. """
        success = []
        self.client.force_login(user=self.user1)
        response = self.client.get(self.url)
        queryset = Board.objects.filter(Q(player_cross=self.user1) | Q(player_circle=self.user1))
        success.extend(
            [
                response.status_code == 200,
                "board/board_list.html" in response.template_name,
                response.context_data["is_paginated"] is False,
                all([item in queryset for item in response.context_data["board_list"]]) and all([item in response.context_data["board_list"] for item in queryset]),
                isinstance(response.context_data["filter"], BoardFilter),
                isinstance(response.context_data["table"], BoardTable),
            ]
        )
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user1.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user1.cross.all())

        self.board.status = 2
        self.board.save()
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.client.logout()
        self.client.force_login(user=self.user2)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 1,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user2.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user2.cross.all())

        self.client.logout()
        self.client.force_login(user=self.user3)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user3.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user3.cross.all())

        self.board.status = 3
        self.board.save()

        self.client.logout()
        self.client.force_login(user=self.user1)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 1,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user1.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user1.cross.all())

        self.client.logout()
        self.client.force_login(user=self.user2)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user2.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user2.cross.all())

        self.client.logout()
        self.client.force_login(user=self.user3)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user3.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user3.cross.all())

        self.board.status = 4
        self.board.save()

        self.client.logout()
        self.client.force_login(user=self.user1)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 1,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user1.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user1.cross.all())

        self.client.logout()
        self.client.force_login(user=self.user2)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 1,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user2.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user2.cross.all())

        self.client.logout()
        self.client.force_login(user=self.user3)
        response = self.client.get(self.url)
        historic_record = [
            response.context_data["victories_as_circle"] == 0,
            response.context_data["draws_as_circle"] == 0,
            response.context_data["victories_as_cross"] == 0,
            response.context_data["draws_as_cross"] == 0,
        ]
        success.extend(historic_record)
        self.assertQuerysetEqual(response.context_data["boards_as_circle"], self.user3.circle.all())
        self.assertQuerysetEqual(response.context_data["boards_as_cross"], self.user3.cross.all())

        self.assertTrue(all(success))

    def test_filter(self):
        """ Test to check the filter in the view works properly. """
        success = []
        Board.objects.bulk_create([
            Board(player_circle=self.user1, player_cross=self.user2, status=2),
            Board(player_circle=self.user1, player_cross=self.user2, status=3),
            Board(player_circle=self.user1, player_cross=self.user2, status=4),
            Board(player_circle=self.user2, player_cross=self.user1, status=1),
            Board(player_circle=self.user2, player_cross=self.user1, status=2),
            Board(player_circle=self.user2, player_cross=self.user1, status=3),
            Board(player_circle=self.user2, player_cross=self.user1, status=4),
        ])
        url = self.url + "?player_type=cross"
        self.client.force_login(user=self.user1)
        response = self.client.get(url)
        queryset = Board.objects.filter(Q(player_cross=self.user1))
        self.assertQuerysetEqual(queryset, response.context_data["board_list"])

        url = self.url + "?player_type=circle"
        response = self.client.get(url)
        queryset = Board.objects.filter(Q(player_circle=self.user1))
        self.assertQuerysetEqual(queryset, response.context_data["board_list"])

        url = self.url + "?won=won"
        response = self.client.get(url)
        queryset = Board.objects.filter(Q(player_cross=self.user1, status=2) | Q(player_circle=self.user1, status=3))
        self.assertQuerysetEqual(queryset, response.context_data["board_list"])

        url = self.url + "?won=loss"
        response = self.client.get(url)
        queryset = Board.objects.filter(Q(player_cross=self.user1, status=3) | Q(player_circle=self.user1, status=2))
        self.assertQuerysetEqual(queryset, response.context_data["board_list"])

        url = self.url + "?won=draw"
        response = self.client.get(url)
        queryset = Board.objects.filter(Q(player_cross=self.user1, status=4) | Q(player_circle=self.user1, status=4))
        self.assertQuerysetEqual(queryset, response.context_data["board_list"])

