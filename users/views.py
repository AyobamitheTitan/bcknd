from django.db.models import Count, F, IntegerField
from django.db.models.expressions import ExpressionWrapper
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bins.models import BinModel


# Create your views here.
class UserLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        bins = (
            BinModel.objects
            .values("uploaded_by")
            .annotate(bin_count=Count("id"))
            .annotate(points=ExpressionWrapper(F("bin_count") * 10, output_field=IntegerField()))
            .order_by("-bin_count")
            .annotate(
                username=F("uploaded_by__username"),
                email=F("uploaded_by__email"),
            )
            .values("username","email" ,"points")
        )
        return Response({"data":bins, "message":"Successful"})