from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from healthcare_ms.users.serializers import UserRegistrationSerializer, DetailUserAdminSerializer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully.",
                "data": DetailUserAdminSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to register user.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
