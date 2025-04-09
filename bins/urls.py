from django.urls import path

from .views import BinView, BinLocationView

urlpatterns = [
    path("", BinView.as_view()),
    path("/locations", BinLocationView.as_view())
]