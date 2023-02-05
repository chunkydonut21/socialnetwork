from django.urls import path, include
from chat.views import ChatView, ChatList

app_name = 'chat'

urlpatterns = [
    path('chat_list', ChatList.as_view(), name='chat_list'),
    path('chat_room/<str:username>/', ChatView.as_view(), name='chat_room')
]