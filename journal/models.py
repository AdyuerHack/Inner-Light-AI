from django.db import models
from django.contrib.auth.models import User
from PIL import Image  # para optimizar imágenes en CommunityPost


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280, blank=True, null=True)
    image = models.ImageField(upload_to='community/images/', blank=True, null=True)
    video = models.FileField(upload_to='community/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        base = (self.content or "").strip()
        return base[:60] if base else f"Post {self.id} (sin texto)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                path = self.image.path
                with Image.open(path) as img:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.thumbnail((1200, 1200), Image.LANCZOS)
                    img.save(path, optimize=True, quality=85)
            except Exception:
                pass


class CommunityComment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comentario de {self.user.username} en post {self.post_id}"


class Reaction(models.Model):
    REACTION_CHOICES = [
        ('heart', '❤️'),
        ('laugh', '😂'),
        ('pray',  '🙏'),
        ('sad',   '😢'),
        ('light', '🌟'),
    ]
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'reaction_type', 'user')

    def __str__(self) -> str:
        return f"{self.user.username} reaccionó {self.reaction_type} al post {self.post_id}"


# --------- Resultados de análisis de IA sobre el diario (se mantiene tu diseño) ----------
class JournalAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_analyses')
    # Guardamos JSON serializado como texto:
    result_json = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Análisis {self.id} - {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
