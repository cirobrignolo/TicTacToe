from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Game, Movement
from .serializers import GameSerializer, MovementSerializer
from rest_framework.exceptions import NotFound

# Game only need the list, retrieve and create actions
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

# Movements only need the list and create actions
class MovementViewSet(viewsets.ModelViewSet):

    # list all the movements of a game if exists
    def list(self, request, *args, **kwargs):
        game_id = self.kwargs.get('game_id')
        try:
            Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response({'detail': 'Game not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = Movement.objects.filter(game_id=game_id)
        serializer = MovementSerializer(queryset, many=True)
        return Response(serializer.data)

    # Creates a movement for an specific game if exists
    def create(self, request, *args, **kwargs):
        game_id = self.kwargs.get('game_id')
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response({'detail': 'Game not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovementSerializer(data=request.data, context={'game': game})

        if serializer.is_valid():
            serializer.save(game=game)
            game_serializer = GameSerializer(game)
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
