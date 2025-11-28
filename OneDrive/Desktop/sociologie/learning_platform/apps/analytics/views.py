from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserAnalytics, CourseAnalytics, LearningPath, DailyMetric, PerformanceMetric
from .serializers import (
    UserAnalyticsSerializer, CourseAnalyticsSerializer, LearningPathSerializer,
    DailyMetricSerializer, PerformanceMetricSerializer
)

class UserAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter l'analytique utilisateur"""
    serializer_class = UserAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAnalytics.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_analytics(self, request):
        """Récupérer l'analytique de l'utilisateur actuel"""
        try:
            analytics = UserAnalytics.objects.get(user=request.user)
            serializer = self.get_serializer(analytics)
            return Response(serializer.data)
        except UserAnalytics.DoesNotExist:
            return Response({'error': 'Analytique non trouvée'}, status=404)


class CourseAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter l'analytique des cours"""
    queryset = CourseAnalytics.objects.all()
    serializer_class = CourseAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]


class LearningPathViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les parcours d'apprentissage"""
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les métriques quotidiennes"""
    serializer_class = DailyMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return DailyMetric.objects.filter(user=self.request.user)


class PerformanceMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les métriques de performance"""
    serializer_class = PerformanceMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PerformanceMetric.objects.filter(user=self.request.user)
