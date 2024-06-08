from django.contrib import admin
from .models import Plank_data

class Plank_dataAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'average_similarity')
    search_fields = ('user__username',)
    list_filter = ('timestamp', 'average_similarity')

admin.site.register(Plank_data, Plank_dataAdmin)