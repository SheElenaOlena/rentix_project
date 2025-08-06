from django.contrib import admin
from django.contrib.auth.models import User as DefaultUser
from apps.users.models import User

# @admin.register(User)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'role', 'is_staff', 'is_active')
#     search_fields = ('email', 'role')
#
#

from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.register(User)