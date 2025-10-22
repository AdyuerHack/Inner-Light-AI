from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Meditation, MeditationSession
import json

def meditation_list(request):
    """Lista de meditaciones disponibles"""
    emotion = request.GET.get('emotion', None)
    
    if emotion:
        meditations = Meditation.objects.filter(is_active=True, emotion_target=emotion)
    else:
        meditations = Meditation.objects.filter(is_active=True)
    
    # Agrupar por emoción
    meditations_by_emotion = {}
    for med in meditations:
        emotion_key = med.emotion_target
        if emotion_key not in meditations_by_emotion:
            meditations_by_emotion[emotion_key] = []
        meditations_by_emotion[emotion_key].append(med)
    
    return render(request, "meditation/list.html", {
        "meditations_by_emotion": meditations_by_emotion,
        "selected_emotion": emotion
    })

def meditation_detail(request, meditation_id):
    """Vista de una meditación específica"""
    meditation = get_object_or_404(Meditation, id=meditation_id, is_active=True)
    
    # Obtener sesiones previas del usuario
    previous_sessions = None
    if request.user.is_authenticated:
        previous_sessions = MeditationSession.objects.filter(
            user=request.user,
            meditation=meditation,
            completed=True
        )[:5]
    
    return render(request, "meditation/detail.html", {
        "meditation": meditation,
        "previous_sessions": previous_sessions
    })

@require_POST
def start_session(request, meditation_id):
    """Iniciar sesión de meditación"""
    meditation = get_object_or_404(Meditation, id=meditation_id)
    user = request.user if request.user.is_authenticated else None
    
    # Obtener emoción antes de la meditación
    emotion_before = request.POST.get('emotion_before', '')
    
    session = MeditationSession.objects.create(
        user=user,
        meditation=meditation,
        emotion_before=emotion_before
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'session_id': session.id
        })
    
    return redirect('meditation:detail', meditation_id=meditation_id)

@require_POST
def complete_session(request, session_id):
    """Completar sesión de meditación"""
    session = get_object_or_404(MeditationSession, id=session_id)
    
    # Verificar permisos
    if session.user and session.user != request.user:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    try:
        data = json.loads(request.body) if request.body else {}
        
        session.completed = True
        session.emotion_after = data.get('emotion_after', '')
        session.duration_actual = data.get('duration_actual', session.meditation.duration_minutes)
        session.notes = data.get('notes', '')
        session.save()
        
        return JsonResponse({
            'success': True,
            'message': '¡Sesión completada! ¿Cómo te sientes ahora?'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def my_sessions(request):
    """Historial de sesiones del usuario"""
    if not request.user.is_authenticated:
        return redirect('meditation:list')
    
    sessions = MeditationSession.objects.filter(
        user=request.user,
        completed=True
    )[:50]
    
    # Estadísticas
    total_minutes = sum(s.duration_actual or s.meditation.duration_minutes for s in sessions)
    
    stats = {
        'total_sessions': sessions.count(),
        'total_minutes': total_minutes,
        'total_hours': round(total_minutes / 60, 1)
    }
    
    return render(request, "meditation/my_sessions.html", {
        "sessions": sessions,
        "stats": stats
    })
