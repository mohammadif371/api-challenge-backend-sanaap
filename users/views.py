from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, CreateUserSerializer
from .permissions import IsAdmin


class LoginView(APIView):
    permission_classes = []  # public endpoint

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


class UserListView(generics.ListAPIView):
    """Only admin can see all users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]