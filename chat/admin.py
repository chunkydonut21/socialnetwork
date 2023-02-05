from django.contrib import admin
from chat.models import Chat, ChatMessage


# Register your models here.

class MessageInline(admin.TabularInline):
    model = ChatMessage


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    inlines = (MessageInline,)


admin.site.register(Chat, ChatAdmin)
