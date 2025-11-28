from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import EmotionDetection, EmotionalState, EmotionAdaptation, EmotionFeedback, EmotionalTrend
from .serializers import (
    EmotionDetectionSerializer, EmotionalStateSerializer, EmotionAdaptationSerializer,
    EmotionFeedbackSerializer, EmotionalTrendSerializer
)

class EmotionDetectionViewSet(viewsets.ModelViewSet):
    """ViewSet pour la détection d'émotions"""
    serializer_class = EmotionDetectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmotionDetection.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upload_emotion_data(self, request):
        """Upload les données de détection émotionnelle"""
        if not request.user.emotion_tracking_enabled:
            return Response({'error': 'Suivi émotionnel désactivé'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            emotion = serializer.save(user=request.user)
            
            # Déclencher les adaptations si nécessaire
            self._trigger_adaptations(request.user, emotion)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def recent_emotions(self, request):
        """Récupérer les émotions récentes"""
        hours = request.query_params.get('hours', 24)
        since = timezone.now() - timedelta(hours=int(hours))
        emotions = self.get_queryset().filter(created_at__gte=since)
        serializer = self.get_serializer(emotions, many=True)
        return Response(serializer.data)
    
    def _trigger_adaptations(self, user, emotion):
        """Déclencher les adaptations basées sur l'émotion"""
        # Cette logique sera implémentée dans le module IA
        pass


class EmotionalStateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour l'état émotionnel agrégé"""
    serializer_class = EmotionalStateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmotionalState.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current_state(self, request):
        """Obtenir l'état émotionnel actuel"""
        try:
            state = EmotionalState.objects.get(user=request.user)
            serializer = self.get_serializer(state)
            return Response(serializer.data)
        except EmotionalState.DoesNotExist:
            return Response({'error': 'État non disponible'}, status=status.HTTP_404_NOT_FOUND)


class EmotionAdaptationViewSet(viewsets.ModelViewSet):
    """ViewSet pour les adaptations émotionnelles"""
    serializer_class = EmotionAdaptationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmotionAdaptation.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept_adaptation(self, request, pk=None):
        """Accepter une adaptation recommandée"""
        adaptation = self.get_object()
        adaptation.user_accepted = True
        adaptation.applied_at = timezone.now()
        adaptation.save()
        return Response({'status': 'adaptation accepted'})
    
    @action(detail=True, methods=['post'])
    def rate_adaptation(self, request, pk=None):
        """Noter l'efficacité d'une adaptation"""
        adaptation = self.get_object()
        rating = request.data.get('rating')
        if rating:
            adaptation.effectiveness = rating
            adaptation.save()
            return Response({'status': 'adaptation rated'})
        return Response({'error': 'Rating required'}, status=status.HTTP_400_BAD_REQUEST)


class EmotionFeedbackViewSet(viewsets.ModelViewSet):
    """ViewSet pour le feedback utilisateur"""
    serializer_class = EmotionFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmotionFeedback.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmotionalTrendViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les tendances émotionnelles"""
    serializer_class = EmotionalTrendSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmotionalTrend.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def last_7_days(self, request):
        """Tendances des 7 derniers jours"""
        since = timezone.now().date() - timedelta(days=7)
        trends = self.get_queryset().filter(date__gte=since)
        serializer = self.get_serializer(trends, many=True)
        return Response(serializer.data)
