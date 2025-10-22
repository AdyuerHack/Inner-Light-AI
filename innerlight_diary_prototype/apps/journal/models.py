from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    # user es opcional para permitir uso sin login en MVP
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # identificador anónimo derivado de cookie; permite aislar entradas por usuario sin PII
    anon_id = models.CharField(max_length=64, blank=True, default="")
    content = models.TextField()
    sentiment_label = models.CharField(max_length=12, blank=True, default="")
    sentiment_score = models.FloatField(null=True, blank=True)
    tone = models.CharField(max_length=32, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        who = self.user.username if self.user else "anon"
        return f"{who} @ {self.created_at:%Y-%m-%d}"


class CommunityPost(models.Model):
    anon_id = models.CharField(max_length=64, blank=True, default="")
    content = models.TextField()
    mood = models.CharField(max_length=16, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        preview = (self.content[:27] + "…") if len(self.content) > 28 else self.content
        return f"post[{self.mood}] {preview}"
