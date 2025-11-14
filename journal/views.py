from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import json
import requests

from .models import (
    JournalEntry, CommunityPost, CommunityComment, Reaction, JournalAnalysis
)
from .forms import CommunityPostForm


# ------------------------------------------------------
#                       DIARIO
# ------------------------------------------------------

@login_required
def journal_list(request):
    """
    Pantalla principal del diario en formato tipo chat:
    - Muestra las entradas del usuario como si fueran mensajes.
    - Muestra el último análisis espiritual como respuesta de la IA.
    """
    entries = JournalEntry.objects.filter(user=request.user).order_by('created_at')

    # Crear nueva entrada (mensaje del usuario)
    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        if content:
            JournalEntry.objects.create(user=request.user, content=content)
            messages.success(request, '✨ Tu pensamiento fue guardado en el hilo.')
            return redirect('journal:list')
        else:
            messages.warning(request, 'Tu mensaje está vacío.')

    # Cargar último análisis
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
    Recolecta TODAS las entradas del usuario, llama a DeepSeek con el prompt espiritual
    y guarda el resultado estructurado en JSON (último análisis).
    """
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
        JournalAnalysis.objects.create(
            user=request.user,
            result_json=json.dumps({"_warning": "No hay entradas suficientes para analizar."})
        )
        messages.warning(request, "No hay entradas para analizar todavía.")
        return redirect('journal:list')

    joined_text = "\n\n".join(
        [f"[{e['created_at']:%Y-%m-%d %H:%M}] {e['content']}" for e in entries]
    )

    system = (
        "Eres INNER-LIGHT-AI, un mentor y coach espiritual experto en "
        "biocodificación, psicoanálisis, Un Curso de Milagros y simbología mental-espiritual. "
        "Debes responder SOLO en JSON válido UTF-8, sin texto adicional fuera del JSON. "
        "El JSON final debe tener exactamente estas claves:\n\n"
        "{\n"
        '  "estado_emocional_central": "string",\n'
        '  "patrones_pensamiento": ["lista", "de", "strings"],\n'
        '  "creencias_limitantes": ["lista", "de", "strings"],\n'
        '  "herida_emocional_raiz": "string",\n'
        '  "interpretacion_espiritual": "string",\n'
        '  "consejo_practico": "string",\n'
        '  "consejo_espiritual": "string",\n'
        '  "meditacion_guiada": "string"\n'
        "}\n\n"
        "Si hay poca información, rellena con strings cortos o listas vacías, "
        "pero respeta siempre la estructura."
    )

    user_prompt = f"""
Lee las siguientes entradas del diario del usuario y realiza un análisis profundo
desde la biocodificación, el psicoanálisis, Un Curso de Milagros y la simbología espiritual.

Tu misión:
- Detectar la emoción central.
- Identificar patrones de pensamiento.
- Revelar creencias limitantes.
- Conectar con la herida emocional raíz.
- Dar una interpretación espiritual amorosa.
- Ofrecer un consejo práctico y uno espiritual.
- Crear una mini meditación guiada (6–10 líneas) en segunda persona,
  que lo lleve de la confusión a la paz y reconexión con la abundancia interior.

Recuerda: la salida DEBE cumplir exactamente con las claves JSON indicadas.

Diario del usuario:
{joined_text}
""".strip()

    url = f"{base_url.rstrip('/')}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
        "max_tokens": 1500,
    }

    warning = None
    error = None
    result_payload = {}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)

        if resp.status_code != 200:
            error = f"DeepSeek devolvió {resp.status_code}: {resp.text[:300]}"
        else:
            data = resp.json()
            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if not content:
                warning = "La IA no devolvió contenido."
                result_payload = {}
            else:
                try:
                    result_payload = json.loads(content)
                except Exception:
                    error = "La IA devolvió texto que no es JSON válido. Guardado como 'raw_text'."
                    result_payload = {"raw_text": content}

    except requests.Timeout:
        error = "Timeout al contactar DeepSeek."
    except Exception as ex:
        error = f"Error al contactar DeepSeek: {ex}"

    if warning:
        result_payload["_warning"] = warning
    if error:
        result_payload["_error"] = error

    JournalAnalysis.objects.create(
        user=request.user,
        result_json=json.dumps(result_payload, ensure_ascii=False)
    )

    if error:
        messages.error(request, f"Análisis generado con errores: {error}")
    elif warning:
        messages.warning(request, warning)
    else:
        messages.success(request, "✨ Análisis espiritual generado correctamente.")

    return redirect('journal:list')


@login_required
def edit_entry(request, entry_id):
    """
    Permite editar el contenido de una entrada del diario del usuario.
    """
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        if not content:
            messages.warning(request, "El contenido no puede estar vacío.")
            return redirect('journal:entry_edit', entry_id=entry.id)

        entry.content = content
        entry.save()
        messages.success(request, "✏️ Entrada actualizada correctamente.")
        return redirect('journal:list')

    return render(request, 'journal/edit_entry.html', {"entry": entry})


@login_required
def delete_entry(request, entry_id):
    """
    Elimina una entrada del diario del usuario.
    Solo acepta POST (enviado desde un pequeño formulario con CSRF).
    """
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        entry.delete()
        messages.success(request, "🗑️ Entrada eliminada.")
    else:
        messages.error(request, "Método no permitido para eliminar la entrada.")

    return redirect('journal:list')


# ------------------------------------------------------
#                       COMUNIDAD
# ------------------------------------------------------

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

    post_form = CommunityPostForm()
    return render(request, 'journal/community.html', {
        'posts': posts,
        'post_form': post_form,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CommunityPostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            if not obj.content and not obj.image and not obj.video:
                messages.warning(request, 'Tu publicación necesita texto, imagen o video.')
                return redirect('journal:community')
            obj.save()
            messages.success(request, '🌿 Tu reflexión fue publicada anónimamente.')
            return redirect('journal:community')
        else:
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
        reaction.delete()
    return redirect('journal:community')
