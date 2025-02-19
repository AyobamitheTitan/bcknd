from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer,
    SignupSerializer
)
# Create your views here.
class LoginView(APIView):
    def post(self, request):
        request_body = LoginSerializer(data=request.data, context={"request":request})
        if not request_body.is_valid():
            return Response(
                {"error":"Invalid data received","message":"Please fill up the missing fields"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # token, created = Token.objects.create(user=request_body.validated_data['user'])
        # if not created:
        #     raise Exception()
        
        return Response({"data":{}}, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request):
        request_body = SignupSerializer(data=request.data)
        if not request_body.is_valid():
            return Response(
                {"error":"Invalid data received","message":"Please fill up the missing fields"},
                status=status.HTTP_400_BAD_REQUEST
            )
        request_body.save()
        return Response({"data": request_body.data,"message":"New user added"}, status=status.HTTP_201_CREATED)
