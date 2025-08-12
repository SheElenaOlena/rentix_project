from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users.models import User
from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdmin, IsLandlordOwnerOrReadOnly
from ..listings.models import Listing
from ..listings.serializers import ListingSerializer


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
            "role": user.role,
            "groups": [group.name for group in user.groups.all()],
            "date_joined": user.date_joined,
            "is_active": user.is_active
        })


"""проверку прав: только админ или модератор мог видеть всех пользователей"""

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsLandlordOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)