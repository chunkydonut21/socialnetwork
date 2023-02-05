from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class UserProfile(models.Model):
    """
    User profile model which consists of fields such as user status, profile visibility, avatar.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars', null=True,
                               default='uploads/avatars/default.png')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    status = models.TextField(max_length=200, null=False, default="Hi, I am using ConnectU.")
    created_at = models.DateTimeField(default=timezone.now)
    profile_visibility = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class UserPost(models.Model):
    """
    User post model which consists of fields such as text, image and author of the post.
    """

    text = models.TextField(max_length=500, null=False)
    image = models.ImageField(upload_to='uploads/posts_pictures', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="user_likes")


class Like(models.Model):
    """
    Like model consists the relation between users and posts. It is used to track likes on a post by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="like_user_posts")
    already_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.post.text}"
