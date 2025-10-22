from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import JournalEntry
from .sentiment_analysis import sentiment_analyzer

def home(request):
    """Página principal del diario emocional"""
    # Mostrar últimas 50 entradas (propias si logueado; si no, a modo demo mostrar todas)
    if request.user.is_authenticated:
        entries = JournalEntry.objects.filter(user=request.user)[:50]
        # Estadísticas básicas
        stats = {
            'total': JournalEntry.objects.filter(user=request.user).count(),
            'this_week': JournalEntry.objects.filter(user=request.user, created_at__gte=timezone.now() - timezone.timedelta(days=7)).count(),
        }
    else:
        entries = JournalEntry.objects.all()[:20]  # Muestra pública limitada
        stats = None
    
    return render(request, "journal/home.html", {
        "entries": entries,
        "stats": stats
    })

@require_POST
def create(request):
    """Crear entrada de diario con análisis de sentimientos automático"""
    content = request.POST.get("content", "").strip()
    if content:
        user = request.user if request.user.is_authenticated else None
        
        # Análisis de sentimientos
        sentiment_result = sentiment_analyzer.analyze(content)
        
        # Crear entrada
        entry = JournalEntry.objects.create(
            user=user,
            content=content,
            sentiment_label=sentiment_result['sentiment_label'],
            sentiment_score=sentiment_result['sentiment_score'],
            tone=sentiment_result['tone']
        )
        
        # Si es AJAX, devolver JSON con recomendaciones
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            meditation_type = sentiment_analyzer.recommend_meditation(sentiment_result)
            return JsonResponse({
                'success': True,
                'entry_id': entry.id,
                'sentiment': sentiment_result,
                'meditation_recommendation': meditation_type
            })
    
    return redirect("journal:home")

def entry_detail(request, entry_id):
    """Ver detalle de una entrada"""
    entry = get_object_or_404(JournalEntry, id=entry_id)
    
    # Verificar permisos
    if entry.user and entry.user != request.user:
        return redirect("journal:home")
    
    return render(request, "journal/entry_detail.html", {"entry": entry})

def analyze_sentiment_api(request):
    """API para análisis de sentimientos en tiempo real"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            
            if len(text) < 3:
                return JsonResponse({'error': 'Texto muy corto'}, status=400)
            
            result = sentiment_analyzer.analyze(text)
            return JsonResponse({
                'success': True,
                'analysis': result
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.utils import timezone
