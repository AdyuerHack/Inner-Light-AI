from django.contrib import admin
from .models import Meditation, MeditationSession

@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):
    list_display = ('title', 'emotion_target', 'duration_minutes', 'is_active', 'created_at')
    list_filter = ('emotion_target', 'duration_minutes', 'is_active')
    search_fields = ('title', 'description')

@admin.register(MeditationSession)
class MeditationSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'meditation', 'completed', 'emotion_before', 'emotion_after', 'created_at')
    list_filter = ('completed', 'emotion_before', 'emotion_after', 'created_at')
    search_fields = ('user__username', 'meditation__title')
