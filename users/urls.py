from django.urls import path

from .views import UserLeaderboardView

urlpatterns = [
    path("leaderboard", UserLeaderboardView.as_view())
]