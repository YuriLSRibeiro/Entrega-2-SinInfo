from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    content = models.TextField(verbose_name='Conteúdo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de publicação')

    class Meta:
        ordering = ['-created_at', '-id']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Post')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Autor')
    text = models.TextField(verbose_name='Comentário')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de publicação')

    class Meta:
        ordering = ['-created_at', '-id']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f'Comentário de {self.author} em {self.post}'
