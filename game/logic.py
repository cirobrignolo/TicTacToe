import random

from jsonschema import ValidationError

from game.models import Movement

# We will use this TicTacToe to create an instance of a game and play one round
class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.board = game.board
    
    # Makes a move for a player if it's posible
    def make_movement(self, x, y, current_player):
        if self.board[x][y] == ".":
            self.board[x][y] = current_player
            return True
        return False

    # If there is an empty cell, the oponent will use one of them randomly
    def opponent_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == "."]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.make_movement(x, y, 'O')
            return x, y

    # Checks if there is a winner: someone is a winner if a row, column, or diagonal contains [X, X, X] or [O, O, O]. 
    # If there are no more moves left, it declares a draw. 
    # If there isn't a winner and there are still moves available, it returns null
    def check_winner(self):
        rows = (self.board[0], self.board[1], self.board[2])
        columns = ([self.board[i][0] for i in range(3)], [self.board[i][1] for i in range(3)], 
                   [self.board[i][2] for i in range(3)])
        diagonals = ([self.board[i][i] for i in range(3)], [self.board[i][2 - i] for i in range(3)])
        lines = rows + columns + diagonals
        if ["X", "X", "X"] in lines:
            return "X"
        if ["O", "O", "O"] in lines:
            return "O"
        if all(cell != "." for row in self.board for cell in row):
            return "Draw"
        return None
    
    # Generates one round of the game: first, player X (us) makes a move if it is valid. 
    # Then, it checks if player X has won. If not, player O (computer) makes a move and checks if player O has won. 
    # Finally, it returns the winner (if there is one) and the board.
    def generate_round(self, x, y):
        if not self.make_movement(x, y, 'X'):
            raise Exception("Invalid movement")

        Movement.objects.create(game=self.game, x=x, y=y, player="X")

        winner = self.check_winner()
        if not winner:
            opponent_move = self.opponent_move()
            if opponent_move is not None:
                Movement.objects.create(game=self.game, x=opponent_move[0], y=opponent_move[1], player="O")
                winner = self.check_winner()

        return (self.board, winner)
    