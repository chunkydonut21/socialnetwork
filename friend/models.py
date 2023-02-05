from django.db import models
from django.contrib.auth.models import User
from socialnetwork.models import UserProfile


# Create your models here.
class FriendRequest(models.Model):
    """
    friend request model with fields :
    sender is the one who sends the friend request
    receiver is the one who receives the friend request
    created_at is the date at which the request is send,
    is_active states whether the friend request is active or not
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    datetime = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(blank=True, null=False, default=True)
