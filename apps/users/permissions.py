from rest_framework import permissions

# 🔐 1. Разрешает редактирование только владельцу объекта
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только владельцу объекта.
    Остальные пользователи имеют доступ только к чтению (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # ✅ Чтение — разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # ✏️ Изменение — только для владельца объекта
        return obj.owner == request.user

# 🏠 2. Разрешено только пользователям с ролью 'landlord'
class IsLandlord(permissions.BasePermission):
    """
    Доступ только для авторизованных пользователей с ролью 'landlord'.
    Использовать для создания, редактирования, удаления объявлений.
    """
    message = "Только арендодатели могут выполнить это действие."

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and (
            request.user.role == 'landlord' or
            request.user.groups.filter(name='Landlord').exists()
            )
        )

# 👤 3. Разрешено только пользователям с ролью 'tenant'
class IsTenant(permissions.BasePermission):
    """
    Доступ только для авторизованных пользователей с ролью 'tenant'.
    Использовать для доступа к просмотру и фильтрации объявлений.
    """
    message = "Только арендаторы могут выполнить это действие."

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and (
            request.user.role == 'tenant' or
            request.user.groups.filter(name='Tenant').exists()
            )
        )

# 🎯 4. Комбинированный класс: только арендодателю, и только к своему объявлению
class IsLandlordOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только арендодателю, который является владельцем объекта.
    Остальным пользователям — только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # ✅ Чтение — для всех
        if request.method in permissions.SAFE_METHODS:
            return True


        # ✏️ Изменение — только арендодатель и только своего объекта
        return (
                request.user.is_authenticated and (
                request.user.role == 'landlord' or
                request.user.groups.filter(name='Landlord').exists()
        ) and obj.owner == request.user
        )


class IsAdmin(permissions.BasePermission):
    """
    Доступ только для пользователей с ролью 'admin' или в группе 'Admin'.
    """

    message = "Только администраторы могут выполнить это действие."

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and (
                request.user.role == 'admin' or
                request.user.groups.filter(name='Admin').exists()
            )
        )
