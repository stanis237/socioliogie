from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Notification

@login_required
def forum(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'social/forum.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Commentaire ajouté!')
            return redirect('post_detail', post_id=post_id)
    
    return render(request, 'social/post_detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(
                author=request.user,
                title=title,
                content=content
            )
            messages.success(request, 'Post créé avec succès!')
            return redirect('forum')
    return render(request, 'social/create_post.html')

@login_required
def notifications(request):
    notifications_list = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Marquer comme lues
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'social/notifications.html', {'notifications': notifications_list})
