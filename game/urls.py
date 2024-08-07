from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, MovementViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('games/<uuid:game_id>/movements/', MovementViewSet.as_view({'get': 'list', 'post': 'create'}), name='game-movements-list'),
]