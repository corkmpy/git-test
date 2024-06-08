from django.db import models
from django.conf import settings

class Squat_data(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='squat_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    average_similarity = models.FloatField()
    count_final = models.IntegerField()