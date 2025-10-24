from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import JournalEntry, CommunityPost, Reaction


@login_required
def journal_list(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            JournalEntry.objects.create(user=request.user, content=content)
            return redirect('journal:list')

    return render(request, 'journal/journal_list.html', {'entries': entries})


@login_required
def journal_entry(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():
            JournalEntry.objects.create(user=request.user, content=content)
            messages.success(request, '✨ Tu pensamiento fue guardado.')
            return redirect('journal:list')
        else:
            messages.warning(request, 'Tu entrada está vacía.')
    return render(request, 'journal/journal_entry.html')


# 🌐 Comunidad anónima (tipo Twitter)
@login_required
def community_feed(request):
    """
    Muestra el muro anónimo con las últimas 50 publicaciones
    y los conteos de reacciones precalculados.
    """
    posts = CommunityPost.objects.all().order_by('-created_at')[:50]

    # Agregamos los conteos de reacciones manualmente
    for post in posts:
        post.heart_count = post.reactions.filter(reaction_type='heart').count()
        post.laugh_count = post.reactions.filter(reaction_type='laugh').count()
        post.pray_count = post.reactions.filter(reaction_type='pray').count()
        post.sad_count = post.reactions.filter(reaction_type='sad').count()
        post.star_count = post.reactions.filter(reaction_type='star').count()

    return render(request, 'journal/community.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():
            CommunityPost.objects.create(user=request.user, content=content)
            messages.success(request, '🌿 Tu reflexión fue publicada anónimamente.')
        else:
            messages.warning(request, 'Tu publicación está vacía.')
    return redirect('journal:community')


@login_required
def react_to_post(request, post_id, reaction_type):
    post = CommunityPost.objects.get(id=post_id)
    reaction, created = Reaction.objects.get_or_create(
        post=post, user=request.user, reaction_type=reaction_type
    )
    if not created:
        reaction.delete()  # Si ya había reaccionado, quita la reacción
    return redirect('journal:community')
