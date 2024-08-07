# game/tests/test_models.py
from django.test import TestCase
from game.models import Game, Movement

class GameModelTests(TestCase):

    def test_initial_board(self):
        """Test that a new Game object has an initial board of 3x3 and all elemens are '.'."""
        game = Game.objects.create()
        expected_board = [["." for _ in range(3)] for _ in range(3)]
        self.assertEqual(game.board, expected_board)
        self.assertTrue(all(cell == "." for row in game.board for cell in row))

    def test_movement_creation(self):
        """Test that a Movement object is created correctly and associated with a Game."""
        game = Game.objects.create()
        movement = Movement.objects.create(game=game, x=1, y=1, player="X")
        self.assertEqual(movement.game, game)
        self.assertEqual(movement.x, 1)
        self.assertEqual(movement.y, 1)
        self.assertEqual(movement.player, "X")

    def test_game_winner(self):
        """Test that the winner is correctly set in a Game object."""
        game = Game.objects.create()
        game.winner = "X"
        game.save()
        self.assertEqual(game.winner, "X")
