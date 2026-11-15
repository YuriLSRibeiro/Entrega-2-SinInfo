import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from blog.models import Post, Comment, Category

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='Post de Teste',
            content='<p>Conteúdo de teste com <strong>HTML</strong></p>'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Post de Teste')
        self.assertIn('<strong>HTML</strong>', self.post.content)
        self.assertEqual(str(self.post), 'Post de Teste')

    def test_post_ordering(self):
        post2 = Post.objects.create(title='Segundo Post', content='Conteúdo')
        post2.created_at = timezone.now() + datetime.timedelta(seconds=10)
        post2.save()
        posts = Post.objects.all()
        self.assertEqual(posts.first(), post2)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Inteligência Artificial',
            description='Tópicos em IA e aprendizado de máquina'
        )
        self.post = Post.objects.create(
            title='Post com Categoria',
            content='Conteúdo'
        )
        self.post.categories.add(self.category)

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Inteligência Artificial')
        self.assertEqual(self.category.name, 'Inteligência Artificial')

    def test_post_category_many_to_many(self):
        self.assertIn(self.category, self.post.categories.all())
        self.assertIn(self.post, self.category.posts.all())


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(title='Post Teste', content='Conteúdo')
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Este é um comentário de teste.'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertIn('testuser', str(self.comment))


class BlogViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='autor', password='password123')
        self.category = Category.objects.create(name='Backend', description='Desenvolvimento backend')
        self.post = Post.objects.create(title='Post Principal', content='<p>Artigo técnico</p>')
        self.post.categories.add(self.category)

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Post Principal')

    def test_post_detail_view_success(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Post Principal')
        self.assertContains(response, 'Backend')

    def test_post_detail_view_404(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_post_create_view_get(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_create_view_post(self):
        data = {
            'title': 'Novo Post via Teste',
            'content': '<p>Conteúdo criado no teste</p>',
            'categories': [self.category.pk]
        }
        response = self.client.post(reverse('post_create'), data=data)
        self.assertEqual(response.status_code, 302)
        new_post = Post.objects.get(title='Novo Post via Teste')
        self.assertIsNotNone(new_post)
        self.assertIn(self.category, new_post.categories.all())

    def test_post_update_view(self):
        data = {
            'title': 'Post Principal Atualizado',
            'content': '<p>Conteúdo atualizado</p>',
            'categories': [self.category.pk]
        }
        response = self.client.post(reverse('post_update', kwargs={'pk': self.post.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Post Principal Atualizado')

    def test_post_delete_view_get(self):
        response = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')
        self.assertContains(response, 'Confirmar Exclusão')

    def test_post_delete_view_post(self):
        post_pk = self.post.pk
        response = self.client.post(reverse('post_delete', kwargs={'pk': post_pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post_pk).exists())

    def test_comment_create_requires_login(self):
        response = self.client.get(reverse('comment_create', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_comment_create_authenticated(self):
        self.client.login(username='autor', password='password123')
        data = {'text': 'Comentário submetido via teste automatizado'}
        response = self.client.post(reverse('comment_create', kwargs={'pk': self.post.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.user).exists())

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_list.html')
        self.assertContains(response, 'Backend')

    def test_category_detail_view_success(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Categoria: Backend')
        self.assertContains(response, 'Post Principal')

    def test_category_detail_view_404(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)
