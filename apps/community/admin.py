from django.contrib import admin
from .models import AnonymousProfile, CommunityPost, PostComment, PostLike

@admin.register(AnonymousProfile)
class AnonymousProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user', 'anonymous_id', 'created_at')
    search_fields = ('display_name', 'user__username')

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'title', 'is_flagged', 'likes_count', 'created_at')
    list_filter = ('category', 'is_flagged', 'created_at')
    search_fields = ('title', 'content', 'author__display_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_flagged', 'created_at')
    list_filter = ('is_flagged', 'created_at')
    search_fields = ('content', 'author__display_name')

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
