from django.contrib import admin
from .models import ViewHistory, SearchHistory, KeywordSearch

admin.site.register(ViewHistory)
admin.site.register(SearchHistory)
admin.site.register(KeywordSearch)
