from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from apps.users.models import User
from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterUserView(generics.CreateAPIView):
    """
    Эндпоинт регистрации нового пользователя.

    Позволяет создать аккаунт на основе email и пароля.
    По умолчанию присваивает роль TENANT (арендатор).
    Доступ открыт без авторизации (AllowAny).
    """
    queryset = User.objects.all()                      # 🔍 Все объекты User для создания
    serializer_class = RegisterUserSerializer          # 🧩 Сериализатор, который обрабатывает входные данные
    permission_classes = (AllowAny,)                   # 🔓 Доступ открыт всем пользователям (даже без токена)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""возвращаем текущего пользователя и его группы"""

class ProfileView(APIView):
    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "groups": [group.name for group in user.groups.all()]
        })
