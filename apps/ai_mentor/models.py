from django.db import models
from django.contrib.auth.models import User
import uuid

class ChatSession(models.Model):
    """Sesión de chat con el mentor IA - anónima por defecto"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_token = models.CharField(max_length=255, unique=True, db_index=True)  # Para usuarios anónimos
    title = models.CharField(max_length=200, default="Nueva conversación")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-updated_at',)
    
    def __str__(self):
        who = self.user.username if self.user else f"anon-{self.session_token[:8]}"
        return f"{who}: {self.title}"

class ChatMessage(models.Model):
    """Mensajes individuales en una sesión de chat"""
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
        ('system', 'Sistema'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True)  # Detectado automáticamente
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
