from django.db import models


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
