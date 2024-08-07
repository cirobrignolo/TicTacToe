from rest_framework import serializers
from .models import Game, Movement
from .logic import TicTacToe

class MovementSerializer(serializers.ModelSerializer):
    x = serializers.IntegerField(min_value=0, max_value=2, required=True)
    y = serializers.IntegerField(min_value=0, max_value=2, required=True)

    class Meta:
        model = Movement
        fields = ['x', 'y', 'created_at', 'player']
        read_only_fields = ['created_at', 'player']


    # The coordinates are required values and must be a value between 0 and 2.
    def validate(self, data):
        x = data.get('x')
        y = data.get('y')
        if x is None or y is None:
            raise serializers.ValidationError("Both 'x' and 'y' coordinates are required.")
        if x > 2 or x < 0:
            raise serializers.ValidationError("'x' coordinate must be a value between 0 and 2")
        if y > 2 or y < 0:
            raise serializers.ValidationError("'y' coordinate must be a value between 0 and 2")
        return data
    
    # When a move is created, the coordinates are validated. Then, the player's move is made. 
    # If there is no winner yet, the opponent makes a move at random. Then the winner is checked again, 
    # and if there is one, it is returned.
    def create(self, validated_data):
        game = self.context['game']
        x = validated_data['x']
        y = validated_data['y']
        
        tic_tac_toe = TicTacToe(game)
        try:
            game.board, game.winner = tic_tac_toe.generate_round(x, y)
            game.save()
            return game
        except Exception as e:
            raise serializers.ValidationError(f"Error creating movement: {str(e)}")

class GameSerializer(serializers.ModelSerializer):
    movements = MovementSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
