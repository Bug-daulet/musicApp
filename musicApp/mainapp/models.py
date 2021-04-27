from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManage(AbstractUser):
    user_img = models.ImageField(upload_to='users_img/', default='NULL')

    def __str__(self):
        return self.username
