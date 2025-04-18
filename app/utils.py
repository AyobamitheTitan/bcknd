from requests.exceptions import ConnectionError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import (
    ParseError, 
    NotAuthenticated,
    ValidationError,
    MethodNotAllowed,
)
from dropbox.exceptions import AuthError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(exc)
    if isinstance(exc, ConnectionError):
        return Response({
            "error":"Connection Timeout",
            "details":{
                "network":["Network request timed out. Check your internet connection."]
            }
        },
        status=status.HTTP_408_REQUEST_TIMEOUT
    )
    if isinstance(exc, ParseError):
        return Response(
            {
                "error": "Invalid JSON format",
                "details": {
                    "body":["Check your JSON syntax and try again."]}
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if isinstance(exc, NotAuthenticated):
        return Response({
            "error":"Not authenticated",
            "details": {
                "authorization": [response.data.get("detail")]
                }
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    if isinstance(exc, InvalidToken):
        return Response({
            "error":"Invalid token",
            "details":{
                "token":"Token is either invalid or expired"
            }
        },
        status=status.HTTP_401_UNAUTHORIZED
    )
    if isinstance(exc, AuthError):
        return Response({
            "error":"Invalid dropbox token",
            "details":{
                "token":"The dropbox token has expired. Please inform the backend developer to generate a new one"
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    if isinstance(exc, ValidationError):
        return Response({
            "error":"Invalid data received",
            "details":exc.get_full_details()
        },
            status=status.HTTP_400_BAD_REQUEST
    )
    if issubclass(type(exc), ObjectDoesNotExist):
        return Response({
            "error":"Not found",
            "details":{str(exc)}
        },
            status=status.HTTP_404_NOT_FOUND
    )
    if issubclass(type(exc), MethodNotAllowed):
        return Response({
            "error":"Method not allowed",
            "details":"Please correct the API verb in use and try again"
        },
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )

    return response
