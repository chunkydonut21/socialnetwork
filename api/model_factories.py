import factory
from django.contrib.auth.models import User
from socialnetwork.models import UserPost, UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    """User test fixture"""

    username = "johndoe"
    first_name = "John"
    last_name = "Doe"

    class Meta:
        model = User


class UserProfileFactory(factory.django.DjangoModelFactory):
    """user profile test fixture"""

    user = factory.SubFactory(UserFactory)
    status = 'Hi there!'
    profile_visibility = False

    class Meta:
        model = UserProfile


class UserPostFactory(factory.django.DjangoModelFactory):
    """user post test fixture"""

    text = "Hi, this is a sample post!"
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = UserPost
