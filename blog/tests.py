from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post


# Create your tests here.
class PostTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='power',
            email='power@gmail.com',
            password='passwd',
        )

        self.post = Post.objects.create(
            title='Post title',
            content='Post content',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='Post theme')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Post title')
        self.assertEqual(f'{self.post.author}', 'power')
        self.assertEqual(f'{self.post.content}', 'Post content')

    def test_post_list_view(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post content')
        self.assertTemplateUsed(response, 'list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('detail/1/'))
        no_response = self.client.get(reverse('detail/1000/'))
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Post title')
        self.assertTemplateUsed(response, 'detail.html')