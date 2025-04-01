from django.db import models
from django.contrib.auth.models import  User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user_image/', default='user_image/default.jpeg', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.filter(user=self.user):
            return  # Prevent duplicate profiles
        super().save(*args, **kwargs)

