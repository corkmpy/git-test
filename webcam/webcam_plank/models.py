from django.db import models
from django.conf import settings

class Plank_data(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plank_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    average_similarity = models.FloatField()
    