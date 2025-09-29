from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TradingUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    testnet = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Trading User"
        verbose_name_plural = "Trading Users"

    def __str__(self):
        return f"{self.user} - {"Activated" if self.is_active else "Deactivated"}"
