from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    description = models.TextField(verbose_name='Описание')
    like_count = models.PositiveIntegerField(default=0, verbose_name='Количество лайков')
    comment_count = models.PositiveIntegerField(default=0, verbose_name='Количество комментариев')

    def __str__(self):
        return '{} - {}'.format(self.author, self.description[:20])


class Image(models.Model):
    post = models.ForeignKey('webapp.Post', related_name='images', on_delete=models.CASCADE, verbose_name='Пост')
    image = models.ImageField(upload_to='post_images', verbose_name='Изображение')

    def __str__(self) -> str:
        return f'{self.post}: {self.image}'

class Comment(models.Model):
    post = models.ForeignKey('webapp.Post', related_name='comments', on_delete=models.CASCADE, verbose_name='Пост')
    author=models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    text = models.TextField(verbose_name='Комментарии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Like(models.Model):
    post = models.ForeignKey('webapp.Post', related_name='likes', on_delete=models.CASCADE, verbose_name='Пост')
    author=models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes', verbose_name='Автор')


class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following', verbose_name='Подписчик')
    following = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers', verbose_name='Подписка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        unique_together = [['follower', 'following']]
