from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ChatSession, ChatMessage
from .ai_service import ai_mentor
from apps.journal.sentiment_analysis import sentiment_analyzer
import json
import secrets

def get_or_create_session_token(request):
    """Obtener o crear token de sesión para usuarios anónimos"""
    session_token = request.session.get('chat_session_token')
    if not session_token:
        session_token = secrets.token_urlsafe(32)
        request.session['chat_session_token'] = session_token
    return session_token

def chat_home(request):
    """Página principal del chat con el mentor IA"""
    # Obtener o crear sesión activa
    if request.user.is_authenticated:
        sessions = ChatSession.objects.filter(user=request.user, is_active=True)[:10]
    else:
        session_token = get_or_create_session_token(request)
        sessions = ChatSession.objects.filter(session_token=session_token, is_active=True)[:10]
    
    # Sesión actual (la más reciente o crear nueva)
    current_session = sessions.first() if sessions.exists() else None
    
    return render(request, "ai_mentor/chat.html", {
        "sessions": sessions,
        "current_session": current_session
    })

def session_detail(request, session_id):
    """Ver una sesión específica de chat"""
    session = get_object_or_404(ChatSession, id=session_id)
    
    # Verificar permisos
    if session.user and session.user != request.user:
        return redirect('ai_mentor:chat_home')
    elif not session.user:
        session_token = get_or_create_session_token(request)
        if session.session_token != session_token:
            return redirect('ai_mentor:chat_home')
    
    messages = session.messages.all()
    
    return render(request, "ai_mentor/session_detail.html", {
        "session": session,
        "messages": messages
    })

@require_POST
def send_message(request):
    """Enviar mensaje al mentor IA"""
    try:
        data = json.loads(request.body) if request.body else request.POST
        message_content = data.get('message', '').strip()
        session_id = data.get('session_id', None)
        
        if not message_content:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)
        
        # Obtener o crear sesión
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id)
        else:
            # Crear nueva sesión
            user = request.user if request.user.is_authenticated else None
            session_token = get_or_create_session_token(request)
            title = ai_mentor.generate_session_title(message_content)
            
            session = ChatSession.objects.create(
                user=user,
                session_token=session_token,
                title=title
            )
        
        # Analizar sentimiento del mensaje
        sentiment_result = sentiment_analyzer.analyze(message_content)
        
        # Guardar mensaje del usuario
        user_message = ChatMessage.objects.create(
            session=session,
            role='user',
            content=message_content,
            sentiment=sentiment_result['sentiment_label']
        )
        
        # Obtener contexto emocional reciente (últimas entradas de diario)
        user_context = None
        if request.user.is_authenticated:
            from apps.journal.models import JournalEntry
            recent_entries = JournalEntry.objects.filter(
                user=request.user
            ).order_by('-created_at')[:3]
            
            if recent_entries:
                user_context = {
                    'recent_sentiment': recent_entries[0].sentiment_label,
                    'recent_emotions': list(set(e.tone for e in recent_entries if e.tone))
                }
        
        # Generar respuesta del mentor
        conversation_history = []
        for msg in session.messages.all()[-10:]:  # Últimos 10 mensajes
            conversation_history.append({
                'role': msg.role,
                'content': msg.content
            })
        
        ai_response = ai_mentor.generate_response(conversation_history, user_context)
        
        # Guardar respuesta del asistente
        assistant_message = ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=ai_response
        )
        
        # Actualizar sesión
        session.save()  # Actualiza updated_at
        
        return JsonResponse({
            'success': True,
            'session_id': str(session.id),
            'user_message': {
                'id': str(user_message.id),
                'content': user_message.content,
                'created_at': user_message.created_at.isoformat()
            },
            'assistant_message': {
                'id': str(assistant_message.id),
                'content': assistant_message.content,
                'created_at': assistant_message.created_at.isoformat()
            }
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def new_session(request):
    """Crear nueva sesión de chat"""
    user = request.user if request.user.is_authenticated else None
    session_token = get_or_create_session_token(request)
    
    session = ChatSession.objects.create(
        user=user,
        session_token=session_token,
        title="Nueva conversación"
    )
    
    return JsonResponse({
        'success': True,
        'session_id': str(session.id)
    })

def my_sessions(request):
    """Historial de sesiones del usuario"""
    if request.user.is_authenticated:
        sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')[:50]
    else:
        session_token = get_or_create_session_token(request)
        sessions = ChatSession.objects.filter(session_token=session_token).order_by('-updated_at')[:20]
    
    return render(request, "ai_mentor/my_sessions.html", {
        "sessions": sessions
    })
