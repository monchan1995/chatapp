from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUser(AbstractUser):
  img = models.ImageField(upload_to="", verbose_name="アイコン", default="media/スクリーンショット_2024-09-19_22.46.28.png")
  
class Talk(models.Model):
    talk = models.CharField(max_length=500)
    talk_from = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="talk_from"
    )
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_to")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)