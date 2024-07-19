from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    
    date_of_birth = models.DateField( auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.email
    
    
class UserToken(models.Model):
    
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    token = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return str(self.user) + ' token' 

    