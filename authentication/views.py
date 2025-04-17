from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken
)
from .serializers import (
    LoginSerializer,
    SignupSerializer,
    UserSerializer
)
# Create your views here.
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        request_body = LoginSerializer(data=request.data, context={"request":request})
        request_body.is_valid(raise_exception=True)

        token = AccessToken.for_user(request_body.validated_data.get("user"))
        refresh_token = RefreshToken.for_user(request_body.validated_data.get("user"))

        user = UserSerializer(request_body.validated_data.get("user"))

        return Response({
            "data":{
                "token": str(token), 
                "refresh_token":str(refresh_token),
                "user":user.data
                },
            "message":"Successful"
            }, 
            status=status.HTTP_200_OK
        )


class SignupView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        request_body = SignupSerializer(data=request.data)
        request_body.is_valid(raise_exception=True)
        request_body.save()
        return Response({"data": request_body.data,"message":"New user added"}, status=status.HTTP_201_CREATED)
