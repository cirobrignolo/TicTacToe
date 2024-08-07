import uuid
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from game.models import Game, Movement

class GameViewSetTests(APITestCase):
    def setUp(self):
        self.game = Game.objects.create()
        self.list_url = reverse('game-list')
        self.detail_url = reverse('game-detail', kwargs={'pk': self.game.id})
        self.invalid_detail_url = reverse('game-detail', kwargs={'pk': uuid.uuid4()})

    def test_create_game(self):
        """Test that the GameViewSet creates a game correctly."""
        response = self.client.post(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 2)

    def test_list_games(self):
        """Test that the GameViewSet lists all the games."""
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_game(self):
        """Test that the GameViewSet returns a specific game."""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.game.id))

    def test_retrieve_invalid_game(self):
        """Test that the GameViewSet returns and exception if the game does not exists."""
        response = self.client.get(self.invalid_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No Game matches the given query.')

class MovementViewSetTests(APITestCase):
    def setUp(self):
        self.game = Game.objects.create()
        self.list_url = reverse('game-movements-list', kwargs={'game_id': self.game.id})
        self.create_url = self.list_url
        self.invalid_list_url = reverse('game-movements-list', kwargs={'game_id': uuid.uuid4()})

    def test_list_movements(self):
        """Test that the MovementViewSet lists all the movements that belong to a game."""
        Movement.objects.create(game=self.game, x=0, y=0, player='X')
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_movements_invalid_game_id(self):
        """Test that the MovementViewSet returns and exception if the game does not exists while listing."""
        response = self.client.get(self.invalid_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Game not found.')

    def test_create_movement_invalid_game_id(self):
        """Test that the MovementViewSet returns and exception if the game does not exists during creation."""
        data = {'x': 1, 'y': 1}
        response = self.client.post(self.invalid_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Game not found.')

    def test_create_movement_invalid_movement(self):
        """Test that the MovementViewSet returns and exception if the movement is invalid."""
        Movement.objects.create(game=self.game, x=0, y=0, player='X')
        self.game.board = [["X",".","."],[".",".","."],[".",".","."]]
        self.game.save()
        data = {'x': 0, 'y': 0}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Error creating movement: Invalid movement')

    def test_create_movement(self):
        """Test that the MovementViewSet creates a movement correctly."""
        data = {'x': 1, 'y': 1}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), 2)
        self.assertEqual(Movement.objects.filter(game=self.game, player="X").count(), 1)
        self.assertEqual(Movement.objects.filter(game=self.game, player="O").count(), 1)
        self.assertEqual(response.data['winner'], None)

    def test_only_one_move_and_winer(self):
        """Test that the MovementViewSet creates a movement correctly and is the only option, and declares player X the winner."""
        Movement.objects.create(game=self.game, x=0, y=0, player='X')
        Movement.objects.create(game=self.game, x=0, y=1, player='X')
        Movement.objects.create(game=self.game, x=1, y=0, player='X')
        Movement.objects.create(game=self.game, x=1, y=1, player='O')
        Movement.objects.create(game=self.game, x=1, y=2, player='O')
        Movement.objects.create(game=self.game, x=2, y=0, player='O')
        Movement.objects.create(game=self.game, x=2, y=1, player='X')
        Movement.objects.create(game=self.game, x=2, y=2, player='O')
        self.game.board = [["X","X","."],["X","O","O"],["O","X","O"]]
        self.game.save()
        data = {'x': 0, 'y': 2}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), 9)
        self.assertEqual(response.data['winner'], "X")

    def test_winer_move(self):
        """Test that the MovementViewSet creates a movement correctly, and declares player X the winner."""
        Movement.objects.create(game=self.game, x=0, y=0, player='X')
        Movement.objects.create(game=self.game, x=0, y=1, player='X')
        Movement.objects.create(game=self.game, x=1, y=0, player='O')
        Movement.objects.create(game=self.game, x=1, y=1, player='O')
        self.game.board = [["X","X","."],["O","O","."],[".",".","."]]
        self.game.save()
        data = {'x': 0, 'y': 2}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), 5)
        self.assertEqual(response.data['winner'], "X")

    def test_draw_move(self):
        """Test that the MovementViewSet creates a movement correctly and declares a draw."""
        Movement.objects.create(game=self.game, x=0, y=0, player='X')
        Movement.objects.create(game=self.game, x=0, y=1, player='O')
        Movement.objects.create(game=self.game, x=1, y=0, player='X')
        Movement.objects.create(game=self.game, x=1, y=1, player='O')
        Movement.objects.create(game=self.game, x=1, y=2, player='O')
        Movement.objects.create(game=self.game, x=2, y=0, player='O')
        Movement.objects.create(game=self.game, x=2, y=1, player='X')
        Movement.objects.create(game=self.game, x=2, y=2, player='X')
        self.game.board = [["X","O","."],["X","O","O"],["O","X","X"]]
        self.game.save()
        data = {'x': 0, 'y': 2}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), 9)
        self.assertEqual(response.data['winner'], "Draw")

    def test_lose_move(self):
        """Test that the MovementViewSet creates a movement correctly, and declares player O the winner."""
        Movement.objects.create(game=self.game, x=0, y=0, player='X')
        Movement.objects.create(game=self.game, x=0, y=1, player='O')
        Movement.objects.create(game=self.game, x=1, y=0, player='X')
        Movement.objects.create(game=self.game, x=1, y=1, player='O')
        Movement.objects.create(game=self.game, x=1, y=2, player='X')
        Movement.objects.create(game=self.game, x=2, y=0, player='O')
        Movement.objects.create(game=self.game, x=2, y=2, player='O')
        self.game.board = [["X","O","."],["X","O","X"],["O",".","O"]]
        self.game.save()
        data = {'x': 0, 'y': 2}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), 9)
        self.assertEqual(response.data['winner'], "O")
