from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    avatar = models.ImageField(upload_to='avatars', verbose_name='Аватар')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='О себе')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    post_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __repr__(self) -> str:
        return self.user.get_full_name()