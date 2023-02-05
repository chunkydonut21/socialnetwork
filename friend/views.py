from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from friend.models import *


# Create your views here.


@login_required
def friend_request_list(request, *args, **kwargs):
    """
    Returning the list of friend requests list of the logged in user

    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    if request.user.is_authenticated:

        # get a list of received friend requests
        received_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)

        # get a list of sent friend requests
        sent_requests = FriendRequest.objects.filter(sender=request.user, is_active=True)

        context = {
            "received_requests": received_requests,
            "sent_requests": sent_requests
        }

        return render(request, "friend/friend_request_list.html", context)

    else:
        messages.error(request, 'User is not authenticated.')


@login_required
def friend_list(request, username, *args, **kwargs):
    """
    Returns a list of friends of a given user


    :param request:
    :param username:
    :param args:
    :param kwargs:
    :return:
    """

    # if the user is authenticated
    if request.user.is_authenticated:

        # get the profile of a logged in user
        user = User.objects.get(username=username)

        # if profile is present, then find the list of all friends associatec with that profile
        if user:

            friends = user.userprofile.friends.all()

            context = {
                'friend_list': friends,
                'logged_in_user': request.user.username == username
            }

            return render(request, "friend/friend_list.html", context)
        else:
            messages.error(request, 'No profile present.')

    else:
        messages.error(request, 'User is not authenticated.')


@login_required
def send_friend_request(request, *args, **kwargs):
    """
    Send a friend request

    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    context = {}

    if request.method == "POST" and request.user.is_authenticated:

        # check if the user exists
        receiver = User.objects.get(username=request.POST["receiver"])

        # get list of friends of a logged in user
        user_friends = request.user.userprofile.friends.all()

        # check if the receiver is already a present of the logged in user
        is_friend = user_friends.filter(username=receiver.username)

        # if already a friend
        if is_friend:
            context['response'] = "Already a friend with the given user."
            return JsonResponse(context)

        # if not a friend
        if not is_friend:

            # check if a friend request is already present
            friend_request = FriendRequest.objects.filter(sender=request.user, receiver=receiver).first()

            # if friend request is present and is active
            if friend_request and friend_request.is_active:
                raise Exception('Friend request already sent')
            # if friend request is present but not active (i.e. they have declined their friend request)
            elif friend_request and not friend_request.is_active:
                # again send them a friend request by activating it
                friend_request.is_active = True
                friend_request.save()
                context['response'] = "Friend request sent successfully."
            else:
                # first time sending friend request
                friend_request = FriendRequest(sender=request.user, receiver=receiver)
                friend_request.save()
                context['response'] = "Friend request sent successfully."
    else:
        context['response'] = "User is not authenticated."

    return JsonResponse(context)


@login_required
def accept_friend_request(request, *args, **kwargs):
    """
    accepting a friend request

    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    context = {}

    if request.method == "POST" and request.user.is_authenticated:

        # get the friend request id
        request_id = request.POST.get("request_id")

        # get the existing friend request
        friend_request = FriendRequest.objects.get(id=request_id)

        if friend_request.receiver != request.user:
            raise Exception("You are not authorized to make this request.")

        sender = friend_request.sender
        receiver = friend_request.receiver

        # accepting the friend request and adding them to both of their respective friend list
        friend_request.sender.userprofile.friends.add(receiver)
        friend_request.receiver.userprofile.friends.add(sender)
        friend_request.is_active = False
        friend_request.save()

        context["response"] = "Friend request accepted successfully."

    else:
        context['response'] = "User is not authenticated."

    return JsonResponse(context)


@login_required
def cancel_friend_request(request, *args, **kwargs):
    """
    Cancelling a friend request

    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    context = {}

    if request.method == "POST" and request.user.is_authenticated:

        # get the friend request id
        request_id = request.POST.get("request_id")

        # get the friend request with the given request id
        friend_request = FriendRequest.objects.get(id=request_id)

        # inactivate the friend request and checking if requested user is the same as the sender
        if friend_request.sender == request.user and friend_request.is_active:

            friend_request.is_active = False
            friend_request.save()
            context["response"] = "Friend request cancelled successfully."

        else:
            context["response"] = "You are not authorized to make this request."
    else:
        context['response'] = "User is not authenticated."

    return JsonResponse(context)


@login_required
def decline_friend_request(request, *args, **kwargs):
    """
    Declining a friend request

    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    context = {}

    if request.method == "POST" and request.user.is_authenticated:

        # get the friend request id
        request_id = request.POST.get("request_id")

        friend_request = FriendRequest.objects.get(id=request_id)

        # decline the friend request by making it inactive
        if friend_request.receiver == request.user:

            friend_request.is_active = False
            friend_request.save()
            context["response"] = "Friend request declined successfully."

        else:
            context["response"] = "You are not authorized to make this request."
    else:
        context['response'] = "User is not authenticated."

    return JsonResponse(context)
