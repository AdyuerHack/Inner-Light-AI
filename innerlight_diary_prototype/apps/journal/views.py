from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import JournalEntry

def home(request):
    # Mostrar últimas 50 entradas (propias si logueado; si no, a modo demo mostrar todas)
    qs = JournalEntry.objects.all()[:50] if not request.user.is_authenticated else JournalEntry.objects.filter(user=request.user)[:50]
    return render(request, "journal/home.html", {"entries": qs})

@require_POST
def create(request):
    content = request.POST.get("content","").strip()
    if content:
        user = request.user if request.user.is_authenticated else None
        JournalEntry.objects.create(user=user, content=content)
    return redirect("journal:home")
