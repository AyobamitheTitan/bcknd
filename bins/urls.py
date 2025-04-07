from django.urls import path

from .views import BinView

urlpatterns = [
    path("", BinView.as_view()),

]