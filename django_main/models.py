from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    organization_name = models.CharField(max_length=400, null=True)