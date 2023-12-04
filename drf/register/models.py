from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, User

# class User(AbstractUser):
    
#     pass


class ShortenedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    shortened_code = models.CharField(max_length=20, unique=True)
    visits_count = models.PositiveIntegerField(default=0)
    qr_code = models.ImageField(upload_to='qr_codes/',blank=True,null=True)
    
    
    def __str__(self):
        return f"{self.user.username}'s Shortened URL {self.Shortened_code}"