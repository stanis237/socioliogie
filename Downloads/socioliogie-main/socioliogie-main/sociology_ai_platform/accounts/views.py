from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Historique
from content.models import Course

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}!')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    user_profile = request.user.profile
    historique = Historique.objects.filter(user=request.user)[:10]
    return render(request, 'accounts/profile.html', {
        'profile': user_profile,
        'historique': historique
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.level = request.POST.get('level', 'beginner')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profil mis à jour avec succès!')
        return redirect('profile')
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

def logout_view(request):
    """Vue personnalisée pour la déconnexion avec message de confirmation"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès. À bientôt!')
    return redirect('login')
