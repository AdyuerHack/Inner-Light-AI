from django import forms
from .models import JournalEntry, CommunityPost, CommunityComment

IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
VIDEO_CONTENT_TYPES = {"video/mp4", "video/webm", "video/ogg"}
MAX_MEDIA_BYTES = 5 * 1024 * 1024  # 5 MB


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Escribe cómo te sientes hoy...'
            }),
        }


class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control emoji-input',
                'rows': 3,
                'placeholder': 'Comparte tus pensamientos 💬 (emojis + imagen o video)'
            }),
            # Inputs ocultos: los disparamos con iconos en la UI
            'image': forms.ClearableFileInput(attrs={
                'id': 'id_image',
                'accept': 'image/*',
                'class': 'visually-hidden',
                'style': 'display:none;',
            }),
            'video': forms.ClearableFileInput(attrs={
                'id': 'id_video',
                'accept': 'video/mp4,video/webm,video/ogg',
                'class': 'visually-hidden',
                'style': 'display:none;',
            }),
        }

    def clean_image(self):
        f = self.cleaned_data.get('image')
        if not f:
            return f
        if getattr(f, "size", 0) > MAX_MEDIA_BYTES:
            raise forms.ValidationError("La imagen es muy pesada (máx. 5 MB).")
        if getattr(f, "content_type", None) not in IMAGE_CONTENT_TYPES:
            raise forms.ValidationError("Formato de imagen no permitido. Usa JPG, PNG o WebP.")
        return f

    def clean_video(self):
        f = self.cleaned_data.get('video')
        if not f:
            return f
        if getattr(f, "size", 0) > MAX_MEDIA_BYTES:
            raise forms.ValidationError("El video es muy pesado (máx. 5 MB).")
        if getattr(f, "content_type", None) not in VIDEO_CONTENT_TYPES:
            raise forms.ValidationError("Formato de video no permitido. Usa MP4, WebM u Ogg.")
        return f


class CommunityCommentForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '✍️ Escribe un comentario...'
            }),
        }
