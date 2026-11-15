from django import forms
from .models import Post


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
