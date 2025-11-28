from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .models import CustomUser, UserProfile, UserSettings, UserActivityLog
from .serializers import (
    CustomUserSerializer, UserRegistrationSerializer, UserSettingsSerializer,
    UserProfileSerializer, UserActivityLogSerializer, UserUpdateSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Enregistrement d'un nouvel utilisateur"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'Utilisateur créé avec succès', 'user_id': str(user.id)},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Récupérer les informations de l'utilisateur actuel"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """Mettre à jour le profil de l'utilisateur actuel"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(CustomUserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def activity(self, request):
        """Récupérer l'historique d'activité de l'utilisateur"""
        limit = request.query_params.get('limit', 50)
        activities = UserActivityLog.objects.filter(user=request.user)[:int(limit)]
        serializer = UserActivityLogSerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def log_activity(self, request):
        """Enregistrer une activité utilisateur"""
        serializer = UserActivityLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def settings(self, request):
        """Récupérer/mettre à jour les paramètres utilisateur"""
        try:
            settings = request.user.settings
        except UserSettings.DoesNotExist:
            settings = UserSettings.objects.create(user=request.user)
        
        if request.method == 'GET':
            serializer = UserSettingsSerializer(settings)
            return Response(serializer.data)
        
        serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def profile_stats(self, request):
        """Récupérer les statistiques du profil"""
        try:
            profile = request.user.detailed_profile
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profil non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def update_last_activity(self, request):
        """Mettre à jour la dernière activité"""
        request.user.last_activity = timezone.now()
        request.user.save()
        return Response({'message': 'Activité mise à jour'})
    
    @action(detail=False, methods=['post'])
    def enable_emotion_tracking(self, request):
        """Activer le suivi émotionnel avec consentement"""
        request.user.emotion_tracking_enabled = True
        request.user.webcam_consent = request.data.get('webcam_consent', False)
        request.user.save()
        return Response({'message': 'Suivi émotionnel activé'})
    
    @action(detail=False, methods=['post'])
    def disable_emotion_tracking(self, request):
        """Désactiver le suivi émotionnel"""
        request.user.emotion_tracking_enabled = False
        request.user.webcam_consent = False
        request.user.save()
        return Response({'message': 'Suivi émotionnel désactivé'})


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les profils utilisateurs"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)
