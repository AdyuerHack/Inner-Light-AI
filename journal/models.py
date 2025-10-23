import uuid
from django.db import models
from django.contrib.auth.models import User

class Journal(models.Model):
    journal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entry_text = models.TextField(verbose_name="Tu reflexión de hoy")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journals")

    def __str__(self):
        return f"Entrada de {self.user.username} - {self.created_at.strftime('%d/%m/%Y')}"

