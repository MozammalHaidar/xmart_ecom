from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Custom_user(AbstractUser):
    email = models.EmailField(max_length=50,unique=True)
    phone = models.CharField(max_length=15,unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    otp = models.PositiveBigIntegerField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_fics/', default='def.png', blank=True, null=True)


    def __str__(self):
        return self.username