from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import BinSerializer
from .models import BinModel


# Create your views here.
class BinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        request_body = BinSerializer(data=request.data)
        if not request_body.is_valid():
            return Response(
                {"error":"Invalid data received","details":request_body.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        request_body.save()
        return Response({"data": request_body.data,"message":"New bin added"}, status=status.HTTP_201_CREATED)


    def get(self, request):
        bins = BinModel.objects.all().values()
        return Response({"data":bins,"message":"Successful"})