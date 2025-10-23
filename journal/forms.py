from django import forms
from .models import Journal

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['entry_text']
        widgets = {
            'entry_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Escribe cómo te sientes hoy...'
            }),
        }
