from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    rank = models.IntegerField(default=0)


class Memo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    text = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
