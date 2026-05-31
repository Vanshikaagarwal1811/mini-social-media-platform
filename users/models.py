from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='default.png'
    )

    followers = models.ManyToManyField(
    'self',
    symmetrical=False,
    related_name='following',
    blank=True
)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users_permissions',
        blank=True
    )

    def __str__(self):
        return self.username


class Post(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    caption = models.TextField()

    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True
    )

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

class Comment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    caption = models.TextField()

    image = models.ImageField(upload_to='posts/', null=True, blank=True)

    likes = models.ManyToManyField(
    User,
    related_name='liked_comments',
    blank=True
)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username}'s Post"