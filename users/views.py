from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, CreateUserSerializer
from .permissions import IsAdmin


class LoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Login with username and password to get JWT token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'role': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: "Invalid credentials"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role
        })


class CreateUserView(generics.CreateAPIView):
    """Only admin can create users"""
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_summary="Create User",
        operation_description="Admin only - Create a new user with a role"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    """Only admin can see all users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_summary="List Users",
        operation_description="Admin only - Get list of all users"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)