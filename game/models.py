import uuid
from django.db import models

# I’m going to use a base model because both the Game and Movement models need an ID (I use uuid for added security) 
# and a creation date so that they can be ordered by this date.
class Base(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

# The game will consist of a board along with the winner, if there is one.
class Game(Base):
    board = models.JSONField(default=dict)
    winner = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return f"Game {self.id} - Winner: {self.winner}"
    
    def save(self, *args, **kwargs):
        # Inicializar el tablero como una tabla de 3x3 si está vacío
        if not self.board:
            self.board = [["." for _ in range(3)] for _ in range(3)]
        super().save(*args, **kwargs)

# The move will be associated with a game and needs to store the coordinates and the player who made the move.
class Movement(Base):
    game = models.ForeignKey(Game, related_name='movements', on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    player = models.CharField(max_length=1)

    def __str__(self):
        return f"Movement by {self.player} at ({self.x}, {self.y})"
    