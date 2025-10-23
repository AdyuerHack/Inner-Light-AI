from django.shortcuts import render, redirect
from .models import Journal
from .forms import JournalForm

def journal_entry(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            # comentar esta línea si no hay usuarios todavía
            # entry.user = request.user
            entry.save()
            return redirect('journal_list')
    else:
        form = JournalForm()
    return render(request, 'journal/journal_entry.html', {'form': form})

def journal_list(request):
    journals = Journal.objects.all().order_by('-created_at')
    return render(request, 'journal/journal_list.html', {'journals': journals})
