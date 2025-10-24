from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post anónimo {self.id}"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('heart', '❤️'),
        ('laugh', '😂'),
        ('pray', '🙏'),
        ('sad', '😢'),
        ('star', '🌟'),
    ]
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'reaction_type', 'user')

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction_type} to post {self.post.id}"
