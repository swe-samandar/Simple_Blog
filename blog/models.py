from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title