from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'friend'

urlpatterns = [

    # friend request page with list of received and sent friend requests
    path('friend_request_list/', login_required(login_url='/login')(views.friend_request_list),
         name='friend_request_list'),

    # friend list page of a given user
    path('friend_list/<str:username>', login_required(login_url='/login')(views.friend_list), name='friend_list'),

    # ajax endpoint to send a post request
    path('send_friend_request/', login_required(login_url='/login')(views.send_friend_request),
         name='send_friend_request'),

    # ajax endpoint to accept a friend request
    path('accept_friend_request/', login_required(login_url='/login')(views.accept_friend_request),
         name='accept_friend_request'),

    # ajax endpoint to cancel a friend request
    path('cancel_friend_request/', login_required(login_url='/login')(views.cancel_friend_request),
         name='cancel_friend_request'),

    # ajax endpoint to decline a friend request
    path('decline_friend_request/', login_required(login_url='/login')(views.decline_friend_request),
         name='decline_friend_request'),
]
