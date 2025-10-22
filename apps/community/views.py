from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import AnonymousProfile, CommunityPost, PostComment, PostLike
import json
import random

# Nombres anónimos aleatorios
ANONYMOUS_NAMES = [
    "Viajero de Luz", "Alma Serena", "Corazón Valiente", "Espíritu Libre",
    "Guardián de Paz", "Buscador Interior", "Llama Eterna", "Río Tranquilo",
    "Montaña Sabia", "Estrella Brillante", "Luna Creciente", "Sol Radiante",
    "Árbol Antiguo", "Flor Resiliente", "Viento Suave", "Océano Profundo"
]

AVATAR_COLORS = [
    "#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f59e0b",
    "#10b981", "#14b8a6", "#06b6d4", "#3b82f6", "#6366f1"
]

def get_or_create_anonymous_profile(request):
    """Obtener o crear perfil anónimo para el usuario"""
    if request.user.is_authenticated:
        profile, created = AnonymousProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'display_name': random.choice(ANONYMOUS_NAMES),
                'avatar_color': random.choice(AVATAR_COLORS)
            }
        )
        return profile
    return None

def community_home(request):
    """Página principal de la comunidad anónima"""
    posts = CommunityPost.objects.filter(is_flagged=False).annotate(
        comments_count=Count('comments')
    )[:50]
    
    category_filter = request.GET.get('category', None)
    if category_filter:
        posts = posts.filter(category=category_filter)
    
    profile = get_or_create_anonymous_profile(request)
    
    return render(request, "community/home.html", {
        "posts": posts,
        "profile": profile,
        "categories": CommunityPost.CATEGORY_CHOICES,
        "selected_category": category_filter
    })

@require_POST
def create_post(request):
    """Crear publicación anónima"""
    profile = get_or_create_anonymous_profile(request)
    
    if not profile:
        return JsonResponse({'error': 'Debes estar autenticado'}, status=403)
    
    try:
        data = json.loads(request.body) if request.body else request.POST
        
        category = data.get('category', 'reflection')
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not content or len(content) < 10:
            return JsonResponse({'error': 'Contenido muy corto'}, status=400)
        
        # Moderación básica automática
        is_flagged, flag_reason = moderate_content(content)
        
        post = CommunityPost.objects.create(
            author=profile,
            category=category,
            title=title,
            content=content,
            is_flagged=is_flagged,
            flag_reason=flag_reason
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'post_id': str(post.id),
                'message': 'Publicación compartida con la comunidad' if not is_flagged else 'Publicación en revisión'
            })
        
        return redirect('community:home')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def post_detail(request, post_id):
    """Ver detalle de publicación con comentarios"""
    post = get_object_or_404(CommunityPost, id=post_id)
    
    if post.is_flagged and (not request.user.is_staff):
        return redirect('community:home')
    
    comments = post.comments.filter(is_flagged=False)
    profile = get_or_create_anonymous_profile(request)
    
    # Verificar si el usuario dio like
    user_liked = False
    if profile:
        user_liked = PostLike.objects.filter(post=post, author=profile).exists()
    
    return render(request, "community/post_detail.html", {
        "post": post,
        "comments": comments,
        "profile": profile,
        "user_liked": user_liked
    })

@require_POST
def add_comment(request, post_id):
    """Agregar comentario anónimo"""
    post = get_object_or_404(CommunityPost, id=post_id)
    profile = get_or_create_anonymous_profile(request)
    
    if not profile:
        return JsonResponse({'error': 'Debes estar autenticado'}, status=403)
    
    try:
        data = json.loads(request.body) if request.body else request.POST
        content = data.get('content', '').strip()
        
        if not content or len(content) < 3:
            return JsonResponse({'error': 'Comentario muy corto'}, status=400)
        
        # Moderación básica
        is_flagged, _ = moderate_content(content)
        
        comment = PostComment.objects.create(
            post=post,
            author=profile,
            content=content,
            is_flagged=is_flagged
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': str(comment.id),
                'author': comment.author.display_name,
                'author_color': comment.author.avatar_color,
                'content': comment.content,
                'created_at': comment.created_at.isoformat()
            }
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def toggle_like(request, post_id):
    """Dar/quitar like a una publicación"""
    post = get_object_or_404(CommunityPost, id=post_id)
    profile = get_or_create_anonymous_profile(request)
    
    if not profile:
        return JsonResponse({'error': 'Debes estar autenticado'}, status=403)
    
    try:
        like, created = PostLike.objects.get_or_create(post=post, author=profile)
        
        if not created:
            # Ya existía, eliminar
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            liked = False
        else:
            # Nuevo like
            post.likes_count += 1
            liked = True
        
        post.save()
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def moderate_content(text: str) -> tuple:
    """
    Moderación automática básica
    Returns: (is_flagged: bool, reason: str)
    """
    text_lower = text.lower()
    
    # Lista de palabras prohibidas (básico para MVP)
    forbidden_words = [
        'suicidio', 'matar', 'morir', 'muerte violenta',
        'drogas ilegales', 'spam', 'publicidad'
    ]
    
    for word in forbidden_words:
        if word in text_lower:
            return (True, f'Contenido sensible detectado: {word}')
    
    # Detectar spam (muchas mayúsculas o repetición)
    if len(text) > 20:
        uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if uppercase_ratio > 0.5:
            return (True, 'Posible spam: exceso de mayúsculas')
    
    return (False, '')
