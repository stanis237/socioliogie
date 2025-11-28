from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import CustomUser
from .serializers import CustomUserSerializer, UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Retourne les données du profil de l'utilisateur connecté"""
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Connexion d'un utilisateur"""
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email et mot de passe requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=email, password=password)
    if user is None:
        return Response(
            {'error': 'Identifiants invalides'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': CustomUserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': CustomUserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Déconnexion d'un utilisateur"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Déconnexion réussie'})
    except Exception:
        return Response({'error': 'Erreur lors de la déconnexion'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    """Rafraîchissement du token d'accès"""
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response(
            {'error': 'Token de rafraîchissement requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        })
    except Exception:
        return Response(
            {'error': 'Token invalide'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """Demande de réinitialisation de mot de passe"""
    email = request.data.get('email')
    if not email:
        return Response(
            {'error': 'Email requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Envoyer l'email de réinitialisation
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
        subject = 'Réinitialisation de votre mot de passe'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return Response({'message': 'Email de réinitialisation envoyé'})
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'Utilisateur non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    """Confirmation de réinitialisation de mot de passe"""
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    if not all([uidb64, token, new_password]):
        return Response(
            {'error': 'Tous les champs sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return Response(
            {'error': 'Lien invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Mot de passe réinitialisé avec succès'})
    else:
        return Response(
            {'error': 'Token invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )
