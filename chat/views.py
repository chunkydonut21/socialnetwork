from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from chat.models import Chat


# Create your views here.

class ChatList(View):

    def get(self, request, **kwargs):

        chat_list = Chat.objects.get_queryset().filter(Q(user1=self.request.user) | Q(user2=self.request.user))
        chat_user_list = []

        for chat in chat_list:
            if chat.user1 != self.request.user:
                chat_user_list.append(chat.user1)
            elif chat.user2 != self.request.user:
                chat_user_list.append(chat.user2)

        context = {
            "chat_list": zip(chat_list, chat_user_list)
        }

        return render(request, 'chat/chat_list.html', context)


class ChatView(View):
    def get_object(self):
        self.user_one = self.request.user
        self.user_two = get_user_model().objects.get(username=self.kwargs.get("username"))

        chat_room = Chat.objects.get_queryset().filter(
            (Q(user1=self.user_one) and Q(user2=self.user_two)) | (
                    Q(user1=self.user_two) and Q(user2=self.user_one)))

        if chat_room.exists():
            return chat_room.first()
        else:
            chat_room = Chat.objects.create(user1=self.request.user, user2=self.user_two)

        return chat_room

    def get(self, request, **kwargs):
        context = {
            "user": self.request.user,
            "chat": self.get_object(),
            "friend": self.user_two,
            "messages": self.get_object().chatmessage_set.all()
        }

        return render(request, 'chat/chat.html', context=context)
