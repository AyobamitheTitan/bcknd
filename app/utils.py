from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ParseError):
        return Response(
            {
                "error": "Invalid JSON format",
                "details": {"body":["Check your JSON syntax and try again."]}
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

    return response
