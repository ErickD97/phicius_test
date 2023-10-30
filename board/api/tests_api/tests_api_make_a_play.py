import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import reverse
from rest_framework.test import APITestCase

from board.forms import CreateBoardForm
from board.models import Board

User = get_user_model()


class MakeAPlayTests(APITestCase):
    """Tests for 'board:api_make_movement' api view."""

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="Erick", password="abc*.123")
        cls.user2 = User.objects.create_user(username="Erick1", password="abc*.123")
        cls.user3 = User.objects.create_user(username="Erick2", password="abc*.123")
        cls.board = Board.objects.create(
            player_circle=cls.user1, player_cross=cls.user2
        )

        cls.url = reverse("board:api_make_movement")

    def test_wrong_payload(self):
        """Test to check that this view reacts correctly in front of a defective payload."""
        success = []
        data_dict = {}
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 412,
                json.loads(response.content)["type"] == "PRECONDITION_FAILED",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )

        data_dict.update({"position": "A_1"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 412,
                json.loads(response.content)["type"] == "PRECONDITION_FAILED",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )

        data_dict.pop("position")
        data_dict.update({"board_id": 1})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 412,
                json.loads(response.content)["type"] == "PRECONDITION_FAILED",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )

        self.assertTrue(all(success))

    def test_validations(self):
        """Test to check all validations work correctly."""
        success = []
        data_dict = {
            "board_id": 1000,
            "position": "A_1",
        }
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 400,
                json.loads(response.content)["type"] == "BAD_REQUEST",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )

        data_dict.update({"board_id": self.board.pk, "position": "D_1"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 400,
                json.loads(response.content)["type"] == "BAD_REQUEST",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )

        data_dict.update({"board_id": self.board.pk, "position": "A_4"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 400,
                json.loads(response.content)["type"] == "BAD_REQUEST",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )

        data_dict.update({"board_id": self.board.pk, "position": "A 1"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 412,
                json.loads(response.content)["type"] == "PRECONDITION_FAILED",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )
        self.board.positions_circle["B"] = [2]
        self.board.nodes.next_player = self.user2
        self.board.save()
        self.board.nodes.save()

        data_dict.update({"board_id": self.board.pk, "position": "B_2"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 400,
                json.loads(response.content)["type"] == "BAD_REQUEST",
                json.loads(response.content).get("errors", None) is not None,
            ]
        )

        self.assertTrue(all(success))

    def test_status_changes(self):
        """
        Test to check this view automatically updates the status of the board after a successfull POST request.
        """
        success = []
        self.client.force_login(user=self.user1)

        # Circle column victory, status expected 3
        self.board.positions_circle["A"] = [1, 2]
        self.board.positions_cross["B"] = [1, 2]
        self.board.save()
        data_dict = {
            "board_id": self.board.pk,
            "position": "A_3",
        }
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 200,
                json.loads(response.content)["success"] is True,
                json.loads(response.content)["message"] == "Your Victory!",
                board.status == 3,
            ]
        )

        # Circle diagonal victory, status expected 3
        self.board.positions_circle["A"], self.board.positions_circle["B"] = [1], [2]
        self.board.positions_cross["C"] = [1, 2]
        self.board.status = 1
        self.board.save()
        data_dict.update({"position": "C_3"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 200,
                json.loads(response.content)["success"] is True,
                json.loads(response.content)["message"] == "Your Victory!",
                board.status == 3,
            ]
        )

        # Cross column victory, status expected 2
        self.client.logout()
        self.client.force_login(user=self.user2)
        self.board.positions_circle["A"], self.board.positions_circle["B"] = [1], [2, 3]
        self.board.positions_cross["C"] = [1, 2]
        self.board.status = 1
        self.board.save()
        data_dict.update({"position": "C_3"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 200,
                json.loads(response.content)["success"] is True,
                json.loads(response.content)["message"] == "Your Victory!",
                board.status == 2,
            ]
        )

        # Circle row victory, status expected 3
        self.client.logout()
        self.client.force_login(user=self.user1)
        self.board.positions_circle["A"], self.board.positions_circle["B"] = [1], [1]
        self.board.positions_cross["C"] = [2, 3]
        self.board.status = 1
        self.board.save()
        data_dict.update({"position": "C_1"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 200,
                json.loads(response.content)["success"] is True,
                json.loads(response.content)["message"] == "Your Victory!",
                board.status == 3,
            ]
        )

        # Draw, status expected 4
        self.client.logout()
        self.client.force_login(user=self.user2)
        (
            self.board.positions_circle["A"],
            self.board.positions_circle["C"],
            self.board.positions_circle["B"],
        ) = ([1, 2], [1, 2], [3])
        (
            self.board.positions_cross["A"],
            self.board.positions_cross["B"],
            self.board.positions_cross["C"],
        ) = ([3], [1], [3])
        self.board.status = 1
        self.board.save()
        data_dict.update({"position": "B_2"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 200,
                json.loads(response.content)["success"] is True,
                json.loads(response.content)["message"] == "Draw.",
                board.status == 4,
            ]
        )

        # Unfinished, status expected 1
        self.client.logout()
        self.client.force_login(user=self.user1)
        (
            self.board.positions_circle["A"],
            self.board.positions_circle["B"],
            self.board.positions_circle["C"],
        ) = ([1, 2], [], [])
        (
            self.board.positions_cross["A"],
            self.board.positions_cross["B"],
            self.board.positions_cross["C"],
        ) = ([3], [1], [])
        self.board.status = 1
        self.board.save()
        data_dict.update({"position": "B_2"})
        response = self.client.post(self.url, data=data_dict)
        board = Board.objects.get(id=self.board.pk)
        success.extend(
            [
                response.status_code == 200,
                json.loads(response.content)["success"] is True,
                json.loads(response.content)["message"]
                == "Great! Now wait for your opponent to play.",
                board.status == 1,
            ]
        )

        self.assertTrue(all(success))
