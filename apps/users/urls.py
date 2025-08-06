from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegisterUserView, UserViewSet, ProfileView

app_name = 'users'
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('', include(router.urls)),  # 👈 здесь подключаем маршруты от роутера

    # path('api/profile/', ProfileView.as_view()),
]

# 📌 Без роутера	Кастомные действия: регистрация, логин и т.д.
# 📌 Почему users лучше без роутера?
# 1. Приложение пользователей часто содержит не ViewSet, а обычные views
# Например, RegisterView, LoginView, LogoutView — это классы на основе APIView, а не ViewSet.
# Django REST Framework router нужен именно для ViewSet (где реализованы list, retrieve, create и т.д.)
# А для обычных views — прописываем вручную:
# python
# path('register/', RegisterView.as_view()),
# path('login/', LoginView.as_view()),

# 2. Гибкий контроль URL-структуры
# Без роутера проще писать кастомные пути, такие как:
#
# /api/users/password-reset/
# /api/users/activate/{token}/
# С router всё маршрутизируется автоматически и может быть неудобно переопределять.