from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Plain CRUD for users:
      GET    /api/users/        -> list
      POST   /api/users/        -> create (invite a user)
      GET    /api/users/{id}/   -> detail
      PATCH  /api/users/{id}/   -> update (e.g. change role, deactivate)
      DELETE /api/users/{id}/   -> remove
    """

    queryset = User.objects.all().order_by("-date_joined")

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer


@api_view(["GET"])
def me(request):
    """GET /api/users/me/ -> the logged-in user's own profile."""
    return Response(UserSerializer(request.user).data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    POST /api/auth/login/  { "username": "...", "password": "..." }

    Returns a token the frontend stores in localStorage as
    "ecogrid_token" (see src/lib/api/client.ts) and sends back as
    "Authorization: Bearer <token>".
    """
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user": UserSerializer(user).data})


@api_view(["POST"])
def logout(request):
    """POST /api/auth/logout/ -> deletes the current token."""
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
