from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry


@login_required
def journal_list(request):
    """
    Muestra todas las entradas del diario del usuario autenticado.
    """
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'journal/journal_list.html', {'entries': entries})


@login_required
def journal_entry(request):
    """
    Permite al usuario crear una nueva entrada en su diario.
    """
    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():
            JournalEntry.objects.create(user=request.user, content=content)
            messages.success(request, '✨ Tu pensamiento fue guardado.')
            return redirect('journal:list')
        else:
            messages.warning(request, 'Tu entrada está vacía.')

    return render(request, 'journal/journal_entry.html')
