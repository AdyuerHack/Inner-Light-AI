from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
import json
import requests

from .models import (
    JournalEntry, CommunityPost, CommunityComment, Reaction, JournalAnalysis
)
from .forms import CommunityPostForm  # ⬅️ necesario para el textbox en Comunidad


# ------------------ Diario ------------------

@login_required
def journal_list(request):
    """
    Lista de entradas del diario + creación inline (sin forms) + muestra
    el último análisis almacenado en JournalAnalysis, limpiando las claves
    privadas (_warning/_error) para el template.
    """
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    # Crear nueva entrada simple (como lo usabas)
    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        if content:
            JournalEntry.objects.create(user=request.user, content=content)
            messages.success(request, '✨ Tu pensamiento fue guardado.')
            return redirect('journal:list')
        else:
            messages.warning(request, 'Tu entrada está vacía.')

    # Cargar último análisis y preparar variables seguras para el template
    last_analysis_obj = JournalAnalysis.objects.filter(user=request.user).first()
    analysis_data = None
    analysis_warning = None
    analysis_error = None
    last_analysis_dt = None

    if last_analysis_obj:
        last_analysis_dt = last_analysis_obj.created_at
        try:
            parsed = json.loads(last_analysis_obj.result_json) if last_analysis_obj.result_json else {}
            if isinstance(parsed, dict):
                analysis_warning = parsed.pop('_warning', None)
                analysis_error = parsed.pop('_error', None)
                analysis_data = parsed
        except Exception:
            analysis_error = "No se pudo leer el resultado del análisis."
            analysis_data = None

    return render(request, 'journal/journal_list.html', {
        'entries': entries,
        'analysis_data': analysis_data,
        'analysis_warning': analysis_warning,
        'analysis_error': analysis_error,
        'last_analysis_dt': last_analysis_dt,
    })


@login_required
def analyze_patterns(request):
    """
    Recolecta entradas del usuario, llama a DeepSeek y guarda un resumen estructurado
    en JournalAnalysis.result_json. Devuelve a la lista con mensajes.
    """
    # 1) Validaciones básicas
    api_key = getattr(settings, 'DEEPSEEK_API_KEY', None)
    model = getattr(settings, 'DEEPSEEK_MODEL', 'deepseek-chat')
    base_url = getattr(settings, 'DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    if not api_key:
        messages.error(request, "Falta configurar la clave de DeepSeek (DEEPSEEK_API_KEY).")
        return redirect('journal:list')

    entries = list(
        JournalEntry.objects
        .filter(user=request.user)
        .order_by('created_at')
        .values('created_at', 'content')
    )
    if not entries:
        # Guardamos un análisis vacío con warning para que el template lo muestre
        JournalAnalysis.objects.create(
            user=request.user,
            result_json=json.dumps({"_warning": "No hay entradas suficientes para analizar."})
        )
        messages.warning(request, "No hay entradas para analizar todavía.")
        return redirect('journal:list')

    # 2) Construir prompt (en español, orientado a salida JSON)
    joined_text = "\n\n".join(
        [f"[{e['created_at']:%Y-%m-%d %H:%M}] {e['content']}" for e in entries]
    )
    system = (
        "Eres un analista de bienestar que identifica patrones emocionales y cognitivos "
        "en diarios personales. Responde SOLO en JSON válido UTF-8, sin texto adicional. "
        "La palabra 'json' está presente para activar el modo JSON. json"
    )
    user_prompt = f"""
Analiza el siguiente diario (entradas cronológicas). Entrega un JSON con estas claves:

- emociones: lista de objetos {{ "nombre": str, "frecuencia": "alta|media|baja", "evidencia": str? }}
- disparadores: lista de objetos {{ "tipo": str, "ejemplos": [str]? }}
- patrones: lista de objetos {{ "nombre": str, "descripcion": str, "frases_representativas": [str]? }}
- necesidades: lista de objetos {{ "descripcion": str, "sugerencias": [str]? }}
- ciclos: lista de objetos {{ "descripcion": str, "secuencia": [str]? }}
- recomendaciones: lista de objetos {{ "practica": str, "frecuencia": str, "pasos": [str]? }}

Si hay pocos datos, usa listas vacías y agrega sugerencias prudentes.
Diario:
{joined_text}
""".strip()

    # 3) Llamar a DeepSeek (OpenAI-compatible /v1/chat/completions)
    url = f"{base_url.rstrip('/')}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,  # p.ej. "deepseek-chat"
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt}
        ],
        # JSON Output de DeepSeek
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
        "max_tokens": 1200,
    }

    warning = None
    error = None
    result_payload = {}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            error = f"DeepSeek devolvió {resp.status_code}: {resp.text[:200]}"
        else:
            data = resp.json()
            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            try:
                result_payload = json.loads(content) if content else {}
            except Exception:
                error = "La respuesta de DeepSeek no fue un JSON válido."
    except requests.Timeout:
        error = "Timeout al contactar DeepSeek."
    except Exception as ex:
        error = f"Error al contactar DeepSeek: {ex}"

    # 4) Guardar resultado estructurado
    if warning:
        result_payload["_warning"] = warning
    if error:
        result_payload["_error"] = error

    JournalAnalysis.objects.create(
        user=request.user,
        result_json=json.dumps(result_payload, ensure_ascii=False)
    )

    # 5) Mensajes al usuario
    if error:
        messages.error(request, f"Análisis generado con errores: {error}")
    else:
        messages.success(request, "🧠 Análisis de patrones generado correctamente con DeepSeek.")

    return redirect('journal:list')


# ------------------ Comunidad ------------------

@login_required
def community_feed(request):
    posts = (
        CommunityPost.objects
        .all()
        .order_by('-created_at')
        .prefetch_related('reactions', 'comments')
    )
    for post in posts:
        post.heart_count = post.reactions.filter(reaction_type='heart').count()
        post.laugh_count = post.reactions.filter(reaction_type='laugh').count()
        post.pray_count = post.reactions.filter(reaction_type='pray').count()
        post.sad_count = post.reactions.filter(reaction_type='sad').count()
        post.light_count = post.reactions.filter(reaction_type='light').count()

    # ⬇️ Enviar el formulario para que el textarea aparezca
    post_form = CommunityPostForm()
    return render(request, 'journal/community.html', {
        'posts': posts,
        'post_form': post_form,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        # Usa el form para mantener validaciones (tamaño/formatos) y los IDs usados por la UI
        form = CommunityPostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            # Evitar posts completamente vacíos
            if not obj.content and not obj.image and not obj.video:
                messages.warning(request, 'Tu publicación necesita texto, imagen o video.')
                return redirect('journal:community')
            obj.save()
            messages.success(request, '🌿 Tu reflexión fue publicada anónimamente.')
            return redirect('journal:community')
        else:
            # Si hay errores, re-render con errores visibles y posts
            posts = (
                CommunityPost.objects
                .all()
                .order_by('-created_at')
                .prefetch_related('reactions', 'comments')
            )
            for post in posts:
                post.heart_count = post.reactions.filter(reaction_type='heart').count()
                post.laugh_count = post.reactions.filter(reaction_type='laugh').count()
                post.pray_count = post.reactions.filter(reaction_type='pray').count()
                post.sad_count = post.reactions.filter(reaction_type='sad').count()
                post.light_count = post.reactions.filter(reaction_type='light').count()
            return render(request, 'journal/community.html', {
                'posts': posts,
                'post_form': form,
            })

    return redirect('journal:community')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        if content:
            CommunityComment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, '💬 Comentario agregado.')
        else:
            messages.warning(request, 'Tu comentario está vacío.')
    return redirect('journal:community')


@login_required
def react_to_post(request, post_id, reaction_type):
    post = get_object_or_404(CommunityPost, id=post_id)
    reaction, created = Reaction.objects.get_or_create(
        post=post, user=request.user, reaction_type=reaction_type
    )
    if not created:
        reaction.delete()  # toggle off
    return redirect('journal:community')
