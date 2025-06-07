from django.db import models
from django.contrib.auth import get_user_model

class PasswordReset(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

