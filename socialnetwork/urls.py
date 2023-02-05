from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    # signup route that displays signup page
    path('signup/', views.user_signup, name='signup'),

    # login route that displays login page
    path('login/', views.user_login, name='login'),

    # logout route to log out user from the application
    path('logout/', views.user_logout, name='logout'),

    # ------ Login is required to query the below endpoints. ------

    # Home page that shows user list of posts by them and their friends.
    path('', login_required(login_url='/login')(views.Home.as_view()), name='home'),

    # Profile page with the username as the query parameter to display their posts and profile information.
    path('profile/<str:username>', login_required(login_url='/login')(views.Profile.as_view()), name='profile'),

    # Edit Profile page to edit their profile information by the logged in user.
    path('profile/edit/', login_required(login_url='/login')(views.EditProfile.as_view()), name='profile-edit'),

    # User search page to display all the users based on the keywords entered by the user.
    path('search/', login_required(login_url='/login')(views.UserSearch.as_view()), name='user-search'),

    # AJAX endpoint to upvote post by the logged in user.
    path('upvote_post/', login_required(login_url='/login')(views.upvote_post),
         name='upvote_post'),
]
