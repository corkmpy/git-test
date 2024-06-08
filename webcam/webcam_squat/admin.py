from django.contrib import admin
from .models import Squat_data

class Squat_dataAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'average_similarity', 'count_final')
    search_fields = ('user__username',)
    list_filter = ('timestamp', 'average_similarity', 'count_final')


admin.site.register(Squat_data, Squat_dataAdmin)
