from django.shortcuts import redirect, render
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from friend.models import FriendRequest
from django.db.models.query_utils import Q
from django.http import JsonResponse


# Create your views here.

@login_required
def user_logout(request):
    """
    Log out user

    :param request:
    :return:
    """

    logout(request)
    return redirect('/login')


def user_login(request):
    """
    Log in user

    :param request:
    :return:
    """

    # redirecting to home page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('/')

    # checking for the request type
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        # authenticating user
        user = authenticate(username=username, password=password)

        # checking if user exists
        if user:
            # check if their account is active
            if user.is_active:
                # login user
                login(request, user)
                messages.success(request, 'Logged in.')

                return redirect('/')
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Incorrect credentials entered.')

    return render(request, 'socialnetwork/login.html')


def user_signup(request):
    """
    Register a new user

    :param request:
    :return:
    """

    # redirecting to home page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        # create user signup and profile form instance with the request values
        user_form = UserSignupForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # checking if the forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            messages.success(request, 'User account created successfully.')

            return redirect('/login')

        else:
            print(user_form.errors, profile_form.errors)
    else:

        # if request is not post, then show the user with a blank forms to fill it
        user_form = UserSignupForm()
        profile_form = UserProfileForm()

    # pass the forms as a context to the template
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'socialnetwork/signup.html', context)


class Home(View):
    def get(self, request, *args, **kwargs):
        """
        Returns the list of post by user and their friends
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # finding the logged in user's profile
        profile = UserProfile.objects.filter(user=request.user).first()

        # checkinf if profile exists
        if profile is not None:

            # finding all friends of logged in user
            user_friends = profile.user.userprofile.friends.all()

            # finding all user posts created by the author and their friends
            feed_posts = UserPost.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by(
                '-created_at')

            # empty Post form
            post_form = PostForm()

            # passing the post list and empty form as a context to the template
            context = {
                'post_list': feed_posts,
                'post_form': post_form
            }

            return render(request, 'socialnetwork/home.html', context)

        else:
            messages.error(request, 'No profile found with the given username.')
            logout(request)
            return redirect('/login')

    def post(self, request, *args, **kwargs):
        """
        Show the post form for logged in user to create and share post
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # creating an instance of post form with request values
        post_form = PostForm(request.POST, request.FILES)

        # finding the logged in user's profile
        profile = UserProfile.objects.filter(user=request.user).first()

        # checking if the form is valid and user is authenticated
        if request.user.is_authenticated & post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            # finding all logged in user's friends
            user_friends = profile.user.userprofile.friends.all()

            # finding all user posts created by the author and their friends
            feed_posts = UserPost.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by(
                '-created_at')

            messages.success(request, 'New post created successfully.')

            # empty Post form
            new_post_form = PostForm()

            # passing the post list and empty form as a context to the template
            context = {
                'post_list': feed_posts,
                'post_form': new_post_form
            }

            return render(request, 'socialnetwork/home.html', context)


class Profile(View):

    def get(self, request, username, *args, **kwargs):

        """
        finds the user profile by the username

        :param request:
        :param username:
        :param args:
        :param kwargs:
        :return:
        """

        # search for the user profile by username
        profile = UserProfile.objects.get(user__username=username)
        # find profile posts created by the user in the descending order
        profile_posts = UserPost.objects.filter(author=profile.user).order_by('-created_at')
        # find the list of friends associated with the profile
        profile_friends = profile.friends.all()

        # checking if the request is authenticated and the logged in user is the same as the profile user
        if request.user.is_authenticated and request.user == profile.user:
            # finding all the friend requests received and sent by the user
            received_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
            sent_requests = FriendRequest.objects.filter(sender=request.user, is_active=True)

            return render(request, 'socialnetwork/profile.html', {
                "user": request.user,
                "profile": profile,
                "post_list": profile_posts,
                "friends": profile_friends,
                "logged_in_user": True,
                "is_friend": False,
                "friend_requests": len(sent_requests) + len(received_requests),
                "show_profile": True
            })

        # if the authenticated user is not same as the profile user
        if request.user.is_authenticated and request.user != profile.user:

            # check if the authenticated user is already friend with a profile user
            check_if_friend = True if profile_friends.filter(username=request.user.username) else False

            if check_if_friend:
                return render(request, 'socialnetwork/profile.html', {
                    "user": request.user,
                    "profile": profile,
                    "post_list": profile_posts,
                    "friends": profile_friends,
                    "logged_in_user": False,
                    "is_friend": check_if_friend,
                    "show_profile": True
                })

            else:
                if validate_request(profile.user, request.user):
                    friend_request_by_user = validate_request(profile.user, request.user)

                    return render(request, 'socialnetwork/profile.html', {
                        "user": request.user,
                        "profile": profile,
                        "post_list": profile_posts,
                        "friends": profile_friends,
                        "logged_in_user": False,
                        "is_friend": check_if_friend,
                        "request_by_user": friend_request_by_user.id,
                        "sent_request": "received_request",
                        "show_profile": profile.profile_visibility
                    })

                elif validate_request(request.user, profile.user):
                    friend_request_receiver = validate_request(request.user,
                                                               profile.user)

                    return render(request, 'socialnetwork/profile.html', {
                        "user": request.user,
                        "profile": profile,
                        "post_list": profile_posts,
                        "friends": profile_friends,
                        "logged_in_user": False,
                        "is_friend": check_if_friend,
                        "request_receiver": friend_request_receiver.id,
                        "sent_request": "send_request",
                        "show_profile": profile.profile_visibility
                    })

                else:

                    return render(request, 'socialnetwork/profile.html', {
                        "user": request.user,
                        "profile": profile,
                        "post_list": profile_posts,
                        "friends": profile_friends,
                        "logged_in_user": False,
                        "is_friend": check_if_friend,
                        "sent_request": "no_request",
                        "show_profile": profile.profile_visibility
                    })


class EditProfile(View):
    def get(self, request, *args, **kwargs):

        """
        displaying edit profile form template with pre filled profile details


        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # finding the logged in user's profile
        profile = UserProfile.objects.filter(user=request.user).first()

        # show the user form and profile form with prefilled values if present as a context to the template
        user_form = UserSignupForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }

        return render(request, 'socialnetwork/profile_edit.html', context)

    def post(self, request, *args, **kwargs):

        """
        retrieving the edit profile form request body and saving it to the database

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # finding the logged in user's profile details
        profile = UserProfile.objects.filter(user=request.user).first()

        # user and profile form with the details submitted by the user
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        # validating user and profile form
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile edited.')

            return redirect(f"/profile/{request.user.username}")

        else:
            print(user_form.errors, profile_form.errors)

            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }

            return render(request, 'socialnetwork/profile_edit.html', context)


class UserSearch(View):

    def get(self, request, *args, **kwargs):
        """
        filtering user profiles based on the search params.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # get the query params
        search = self.request.GET.get('query')

        # search for the users that fulfills the below query
        users = User.objects.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

        # send the filtered users back to the template as a context
        context = {'users': users}

        return render(request, 'socialnetwork/user_search.html', context)


@login_required
def upvote_post(request, *args, **kwargs):
    """
    Upvote / remove upvote users post

    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    context = {}

    # checking for the post request type and if user is authenticated
    if request.method == "POST" and request.user.is_authenticated:

        # getting the post id from the request
        post_id = request.POST.get("post_id")

        # finding the logged in user
        user = User.objects.get(username=request.user.username)

        # finding the post based on the given post id
        post = UserPost.objects.filter(id=post_id).first()

        # raise an exception if post not found with the given post id
        if not post:
            raise Exception("No post found with the given post id.")

        # check if user had already liked the post
        check_existing_like = validate_upvote(user, post)

        # if user has already liked the post then toggle it based on the current status
        if check_existing_like:
            like = Like.objects.get(user=user, post=post)

            if like.already_liked:
                like.already_liked = False
                like.save()
                post.user_likes.remove(user)
                post.save()
                context['response'] = "Post disliked successfully"

            else:
                like.already_liked = True
                like.save()
                post.user_likes.add(user)
                post.save()
                context['response'] = "Post liked successfully"

        # if no existing like is present, then add a like
        else:
            print("called again")
            user_like = Like(user=user, post=post)
            user_like.already_liked = True
            user_like.save()
            post.user_likes.add(user)
            post.save()
            context['response'] = "Post liked successfully"

    return JsonResponse(context)


# validate the friend request
def validate_request(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False


# validate the like request
def validate_upvote(user, post):
    try:
        return Like.objects.get(user=user, post=post)
    except Like.DoesNotExist:
        return False
