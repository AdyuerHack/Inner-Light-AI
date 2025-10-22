from django.db import models
from django.contrib.auth.models import User
import uuid

class AnonymousProfile(models.Model):
    """Perfil anónimo para proteger identidad en la comunidad"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    display_name = models.CharField(max_length=50, help_text="Nombre anónimo generado")
    avatar_color = models.CharField(max_length=7, default="#6366f1")  # Color hex
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.display_name} ({self.anonymous_id})"

class CommunityPost(models.Model):
    """Publicaciones anónimas en la comunidad"""
    CATEGORY_CHOICES = [
        ('reflection', 'Reflexión'),
        ('gratitude', 'Gratitud'),
        ('challenge', 'Desafío'),
        ('victory', 'Victoria'),
        ('question', 'Pregunta'),
        ('support', 'Apoyo'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(AnonymousProfile, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True)
    is_flagged = models.BooleanField(default=False, help_text="Moderación automática")
    flag_reason = models.CharField(max_length=200, blank=True)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"{self.author.display_name}: {self.title or self.content[:50]}"

class PostComment(models.Model):
    """Comentarios anónimos en las publicaciones"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(AnonymousProfile, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return f"{self.author.display_name} on {self.post.id}"

class PostLike(models.Model):
    """Sistema de likes anónimo"""
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(AnonymousProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'author')
    
    def __str__(self):
        return f"{self.author.display_name} likes {self.post.id}"
