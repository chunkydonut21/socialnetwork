from django.urls import path
from . import api

app_name = 'api'

urlpatterns = [
    path('users/', api.UserList.as_view(), name='user_list_api'),
    path('users/<str:user__username>/', api.UserProfileInformation.as_view(), name='profile_api'),
    path('user/', api.CreateProfile.as_view(), name='create_profile_api'),
    path('posts/<str:user__username>/', api.PostList.as_view(), name='posts_api')
]
