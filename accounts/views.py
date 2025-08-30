from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.utils.html import escape
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsAdminUser
from rest_framework import status

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request):
        username = escape(str(request.data.get("username", "")))
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Profile
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Admin user management
@extend_schema(responses=UserSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    """Admin endpoint to list all users"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

from rest_framework import serializers

class RoleUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['member', 'admin'])

@extend_schema(request=RoleUpdateSerializer, responses=UserSerializer)
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user_role(request, user_id):
    """Admin endpoint to update user role"""
    try:
        user_id = int(escape(str(user_id)))
        user = User.objects.get(id=user_id)
        role = escape(str(request.data.get('role', '')))
        if role in ['member', 'admin']:
            user.role = role
            user.save()
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
    except (User.DoesNotExist, ValueError):
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)