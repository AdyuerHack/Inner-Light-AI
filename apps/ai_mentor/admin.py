from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'session_token', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'user__username', 'session_token')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'sentiment', 'created_at')
    list_filter = ('role', 'sentiment', 'created_at')
    search_fields = ('content', 'session__title')
    readonly_fields = ('id', 'created_at')
