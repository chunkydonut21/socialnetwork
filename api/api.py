from .serializers import *
from rest_framework import generics
from socialnetwork.models import UserProfile


class UserList(generics.ListAPIView):
    """
    request type: GET
    :param None
    :return list of users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileInformation(generics.RetrieveAPIView):
    """
    request type: GET
    :param user__username
    :return profile of a given user
    """

    lookup_field = 'user__username'
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer


class CreateProfile(generics.CreateAPIView):
    """
    request type: POST
    :param None
    :return creates a user profile
    """

    serializer_class = ProfileSerializer


class PostList(generics.ListAPIView):
    """
    request type: GET
    :param user__username
    :return list of posts of a given user
    """

    queryset = UserPost.objects.all()
    serializer_class = PostSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(author__username=self.kwargs.get('user__username'))