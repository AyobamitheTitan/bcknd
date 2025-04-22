from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .dropbox import DropboxService
from .serializers import AddBinSerializer, BinSerializer, BinLocationSerializer
from .models import BinModel, BinLocationModel


# Create your views here.
class BinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_body = AddBinSerializer(data=request.data)
        request_body.is_valid(raise_exception=True)

        location = BinLocationModel.objects.get(pk=request_body.data["location_id"])
        if location.capacity <= 0:
            raise ValidationError(detail={"capacity":["This location cannot take any more bins"]})
        
        dbx_service = DropboxService()
        bin_image_url = dbx_service.store_file(request.data["bin_image"])
        new_bin = BinSerializer(data={
            "location":request_body.data["location_id"],
            "bin_url":"bin_image_url",
            "emptied_at":request_body.data["emptied_at"],
            "uploaded_by": request.user.id
        })
        new_bin.is_valid(raise_exception=True)
        new_bin.save()
        
        location.capacity -= 1
        location.save()

        return Response({"data": new_bin.data,"message":"New bin added"}, status=status.HTTP_201_CREATED)


    def get(self, request):
        bins = BinModel.objects.all().values()
        return Response({"data":bins,"message":"Successful"})
    

class BinLocationView(APIView):
    def post(self, request):
        request_body = BinLocationSerializer(data=request.data)
        request_body.is_valid(raise_exception=True)

        if BinLocationModel.objects.filter(
            Q(location=request_body.validated_data["location"])&
            Q(city=request_body.validated_data["city"])&
            Q(state=request_body.validated_data["state"])
        ):
            raise ValidationError(detail={"location":["This location has already been added"]}, code=status.HTTP_400_BAD_REQUEST)

        request_body.save()
        return Response({"data":request_body.data, "message":"New location added"}, status=status.HTTP_201_CREATED)
    

    def get(self, request):
        locations = BinLocationModel.objects.all().values()
        return Response({"data":locations,"message":"Successful"})