from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    subscribers = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name='Подписчики')
