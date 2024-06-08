from django.contrib import admin
from .models import Pushup_data

class Pushup_dataAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'average_similarity', 'count_final')
    search_fields = ('user__username',)
    list_filter = ('timestamp', 'average_similarity', 'count_final')

admin.site.register(Pushup_data, Pushup_dataAdmin)