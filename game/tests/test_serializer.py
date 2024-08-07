# game/tests/test_serializers.py
from rest_framework.test import APITestCase
from game.models import Game, Movement
from game.serializers import MovementSerializer, GameSerializer

class MovementSerializerTests(APITestCase):

    def setUp(self):
        self.game = Game.objects.create()
        self.valid_data = {"x": 1, "y": 1}
        self.invalid_data = {"x": None, "y": None}

    def test_valid_move_serializer(self):
        """Test that the MovementSerializer works correctly with valid data."""
        serializer = MovementSerializer(data=self.valid_data, context={'game': self.game})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Movement.objects.count(), 2)

    def test_invalid_move_serializer(self):
        """Test that the MovementSerializer returns errors with invalid data."""
        serializer = MovementSerializer(data=self.invalid_data, context={'game': self.game})
        self.assertFalse(serializer.is_valid())
        self.assertIn('x', serializer.errors)
        self.assertIn('y', serializer.errors)

class GameSerializerTests(APITestCase):

    def setUp(self):
        self.game = Game.objects.create()
        self.serializer = GameSerializer(instance=self.game)

    def test_game_serializer(self):
        """Test that the GameSerializer serializes a Game object correctly."""
        data = self.serializer.data
        self.assertEqual(data['id'], str(self.game.id))
        self.assertEqual(data['winner'], self.game.winner)
        self.assertEqual(data['board'], self.game.board)
