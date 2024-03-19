from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    # Add any additional fields you want in your custom user model
    email = models.CharField(max_length=250, unique=True, null=False, blank=False)
    access_token = models.CharField(max_length=250, null=True)
    refresh_token = models.CharField(max_length=250, null=True)
    refresh_token_expiry_date = models.DateTimeField(null=True)
    REGISTRATION_CHOICES = [
        ("email", "Email"),
        ("google", "Google"),
    ]
    registration_method = models.CharField(
        max_length=10, choices=REGISTRATION_CHOICES, default="email"
    )

    def __str__(self):
        return self.username


class Task(models.Model):
    task_name = models.CharField(max_length=100)
    start_time = models.DateField()
    end_time = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
