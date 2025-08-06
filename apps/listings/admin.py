from django.contrib import admin
from .models import Listing
from .models import Location


# @admin.register(Location)
# class LocationAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         return False


admin.site.register(Listing)
admin.site.register(Location)

