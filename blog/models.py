from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='posts')
    short_desc = models.CharField(max_length=300)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Message(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)
    sended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sended_at']
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return f"{self.message[:15]} from {self.name}"