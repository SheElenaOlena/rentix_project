from django.contrib.auth.models import AbstractUser, Permission, Group, BaseUserManager, UserManager
from django.db import models
from apps.listings.choices.roles import Role



# class User(AbstractUser):
#     role = models.CharField(max_length=20,
#                             choices=Role.choices(),
#                             default=Role.TENANT
#                             )
#     """
#         username	Email
#         логин при входе	Email
#         пароль	Вводится отдельно, обязателен
#     """
#     email = models.EmailField(unique=True)
#
#     # Устраняем конфликт related_name
#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_groups',
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions',
#         blank=True
#     )
#
#     REQUIRED_FIELDS = []
#     USERNAME_FIELD = 'email'
#
#
#     def __str__(self):
#         return f"{self.email} ({self.role})"
#
#     objects = UserManager()

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email.split('@')[0])  # 👈 авто-username
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', email.split('@')[0])  # 👈 авто-username

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    role = models.CharField(max_length=20,
                            choices=Role.choices(),
                            default=Role.TENANT
                            )
    """
        username	Email
        логин при входе	Email
        пароль	Вводится отдельно, обязателен
    """
    email = models.EmailField(unique=True)

    # Устраняем конфликт related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'


    def __str__(self):
        return f"{self.email} ({self.role})"

    objects = UserManager()
