from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    subscribers = models.ManyToManyField('self', symmetrical=False, verbose_name='Подписчики')
