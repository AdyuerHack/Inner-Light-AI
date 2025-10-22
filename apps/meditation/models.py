from django.db import models
from django.contrib.auth.models import User

class Meditation(models.Model):
    """Meditaciones guiadas simples"""
    EMOTION_CHOICES = [
        ('calm', 'Calma'),
        ('anxious', 'Ansiedad'),
        ('sad', 'Tristeza'),
        ('angry', 'Enojo'),
        ('joyful', 'Alegría'),
        ('neutral', 'Neutral'),
        ('stressed', 'Estrés'),
    ]
    
    DURATION_CHOICES = [
        (3, '3 minutos'),
        (5, '5 minutos'),
        (10, '10 minutos'),
        (15, '15 minutos'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    emotion_target = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    duration_minutes = models.IntegerField(choices=DURATION_CHOICES)
    script = models.TextField(help_text="Guión de la meditación")
    audio_url = models.URLField(blank=True, null=True, help_text="URL del audio (opcional)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('emotion_target', 'duration_minutes')
    
    def __str__(self):
        return f"{self.title} ({self.get_emotion_target_display()} - {self.duration_minutes}min)"

class MeditationSession(models.Model):
    """Registro de sesiones de meditación completadas"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meditation = models.ForeignKey(Meditation, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    duration_actual = models.IntegerField(help_text="Duración real en minutos", null=True, blank=True)
    notes = models.TextField(blank=True)
    emotion_before = models.CharField(max_length=20, blank=True)
    emotion_after = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        who = self.user.username if self.user else "anon"
        return f"{who} - {self.meditation.title} @ {self.created_at:%Y-%m-%d}"
