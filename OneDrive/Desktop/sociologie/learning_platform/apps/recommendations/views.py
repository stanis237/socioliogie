from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import ContentRecommendation, ExerciseRecommendation, AIExplainability
from .serializers import (
    ContentRecommendationSerializer, ExerciseRecommendationSerializer, AIExplainabilitySerializer
)

class ContentRecommendationViewSet(viewsets.ModelViewSet):
    """ViewSet pour les recommandations de contenu"""
    serializer_class = ContentRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ContentRecommendation.objects.filter(user=self.request.user, dismissed=False).order_by('-priority')
    
    @action(detail=False, methods=['get'])
    def get_recommendations(self, request):
        """Récupérer les recommandations personnalisées"""
        limit = request.query_params.get('limit', 5)
        recommendations = self.get_queryset()[:int(limit)]
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_clicked(self, request, pk=None):
        """Marquer une recommandation comme consultée"""
        recommendation = self.get_object()
        recommendation.is_clicked = True
        recommendation.clicked_at = timezone.now()
        recommendation.save()
        return Response({'status': 'marked as clicked'})
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Rejeter une recommandation"""
        recommendation = self.get_object()
        recommendation.dismissed = True
        recommendation.dismissed_at = timezone.now()
        recommendation.save()
        return Response({'status': 'dismissed'})
    
    @action(detail=True, methods=['get'])
    def explanation(self, request, pk=None):
        """Obtenir l'explication IA pour une recommandation"""
        recommendation = self.get_object()
        try:
            explanation = recommendation.explanation
            serializer = AIExplainabilitySerializer(explanation)
            return Response(serializer.data)
        except AIExplainability.DoesNotExist:
            return Response({'error': 'Explication non disponible'}, status=status.HTTP_404_NOT_FOUND)


class ExerciseRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les recommandations d'exercices"""
    serializer_class = ExerciseRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExerciseRecommendation.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_attempted(self, request, pk=None):
        """Marquer un exercice comme tenté"""
        recommendation = self.get_object()
        recommendation.is_attempted = True
        recommendation.attempted_at = timezone.now()
        
        actual_score = request.data.get('score')
        if actual_score:
            recommendation.actual_score = actual_score
            recommendation.is_passed = actual_score >= 70  # 70% = réussi
        
        recommendation.save()
        return Response({'status': 'marked as attempted'})
