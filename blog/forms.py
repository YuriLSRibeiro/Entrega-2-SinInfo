from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'Título',
            'content': 'Conteúdo',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título da postagem'}),
            'content': forms.Textarea(attrs={'placeholder': 'Conteúdo da postagem (HTML permitido)', 'rows': 8}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Comentário',
        }
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Escreva seu comentário aqui...', 'rows': 4}),
        }
