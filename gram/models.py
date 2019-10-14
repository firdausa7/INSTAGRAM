from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Profile(models.Model):
    Name = models.TextField(default="Anonymous")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='users/', default='users/user.png')
    bio = models.TextField(default="Welcome Me!")
