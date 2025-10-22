from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import JournalEntry, CommunityPost
from .utils import analyze_sentiment, ensure_anon_cookie

def home(request):
    # Mostrar últimas 50 entradas del usuario anónimo (o autenticado)
    if request.user.is_authenticated:
        qs = JournalEntry.objects.filter(user=request.user)[:50]
    else:
        anon = request.COOKIES.get("il_anon", "")
        qs = JournalEntry.objects.filter(anon_id=anon)[:50] if anon else []
    resp = render(request, "journal/home.html", {"entries": qs})
    # asegurar cookie anónima para NFR7
    ensure_anon_cookie(request, resp)
    return resp

@require_POST
def create(request):
    content = request.POST.get("content", "").strip()
    resp = redirect("journal:home")
    if not content:
        return resp

    user = request.user if request.user.is_authenticated else None
    anon_id = ensure_anon_cookie(request, resp)
    s = analyze_sentiment(content)
    JournalEntry.objects.create(
        user=user,
        anon_id=anon_id if not user else "",
        content=content,
        sentiment_label=s.label,
        sentiment_score=s.score,
        tone=s.tone,
    )
    return resp


def meditations(request):
    # Simple recomendaciones basadas en último tono/sentimiento
    if request.user.is_authenticated:
        last = JournalEntry.objects.filter(user=request.user).first()
    else:
        anon = request.COOKIES.get("il_anon", "")
        last = JournalEntry.objects.filter(anon_id=anon).first() if anon else None
    ctx = {"last": last}
    resp = render(request, "journal/meditations.html", ctx)
    ensure_anon_cookie(request, resp)
    return resp


def community(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        mood = request.POST.get("mood", "").strip()
        resp = redirect("journal:community")
        if content:
            anon_id = ensure_anon_cookie(request, resp)
            CommunityPost.objects.create(anon_id=anon_id, content=content, mood=mood)
        return resp
    posts = CommunityPost.objects.all()[:50]
    resp = render(request, "journal/community.html", {"posts": posts})
    ensure_anon_cookie(request, resp)
    return resp


def chat(request):
    # MVP: reglas simples basadas en sentimiento de la última entrada
    reply = ""
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        # Una respuesta empática simple
        if message:
            s = analyze_sentiment(message)
            if s.label == "negativo":
                reply = "Siento lo que atraviesas. Probemos 3 respiraciones lentas. ¿Qué necesitas ahora?"
            elif s.label == "positivo":
                reply = "Hermoso. Reconoce y agradece este momento. ¿Qué te gustaría cultivar hoy?"
            else:
                reply = "Te escucho. Estoy contigo. ¿Quieres explorar una breve meditación?"
    return render(request, "journal/chat.html", {"reply": reply})
