from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import JournalEntry, CommunityPost, CommunityComment, Reaction
from .forms import JournalEntryForm, CommunityPostForm, CommunityCommentForm


@login_required
def journal_list(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, '✨ Tu pensamiento fue guardado.')
            return redirect('journal:list')
        messages.warning(request, 'Tu entrada está vacía o es inválida.')
    else:
        form = JournalEntryForm()
    return render(request, 'journal/journal_list.html', {'entries': entries, 'form': form})


@login_required
def journal_entry(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, '✨ Tu pensamiento fue guardado.')
            return redirect('journal:list')
        messages.warning(request, 'Tu entrada está vacía o es inválida.')
    else:
        form = JournalEntryForm()
    return render(request, 'journal/journal_entry.html', {'form': form})


@login_required
def community_feed(request):
    posts = (CommunityPost.objects.all()
             .order_by('-created_at')
             .prefetch_related('reactions', 'comments'))
    for post in posts:
        post.heart_count = post.reactions.filter(reaction_type='heart').count()
        post.laugh_count = post.reactions.filter(reaction_type='laugh').count()
        post.pray_count = post.reactions.filter(reaction_type='pray').count()
        post.sad_count = post.reactions.filter(reaction_type='sad').count()
        post.light_count = post.reactions.filter(reaction_type='light').count()

    return render(request, 'journal/community.html', {
        'posts': posts,
        'post_form': CommunityPostForm(),
        'comment_form': CommunityCommentForm(),
    })


@login_required
def create_post(request):
    if request.method != 'POST':
        return redirect('journal:community')

    form = CommunityPostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user

        has_text = bool((post.content or '').strip())
        has_image = bool(post.image)
        has_video = bool(post.video)

        if not (has_text or has_image or has_video):
            messages.warning(request, 'Tu publicación necesita texto, imagen o video.')
            return redirect('journal:community')

        post.save()
        messages.success(request, '🌿 Tu publicación fue enviada.')
        return redirect('journal:community')

    # Errores específicos
    if form.errors.get('image'):
        messages.error(request, f"Imagen: {form.errors['image'].as_text().replace('* ', '')}")
    if form.errors.get('video'):
        messages.error(request, f"Video: {form.errors['video'].as_text().replace('* ', '')}")
    if not (form.errors.get('image') or form.errors.get('video')):
        messages.error(request, 'Revisa el formulario de publicación.')
    return redirect('journal:community')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    if request.method != 'POST':
        return redirect('journal:community')

    form = CommunityCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        messages.success(request, '💬 Comentario agregado.')
    else:
        messages.error(request, 'No se pudo agregar el comentario.')
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
