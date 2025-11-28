from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, NotificationPreference, NotificationSchedule
from .serializers import (
    NotificationSerializer, NotificationPreferenceSerializer, NotificationScheduleSerializer
)

class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).exclude(is_archived=True)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Récupérer les notifications non lues"""
        unread = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(unread, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Obtenir le nombre de notifications non lues"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marquer une notification comme lue"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'status': 'marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_as_clicked(self, request, pk=None):
        """Marquer une notification comme cliquée"""
        notification = self.get_object()
        notification.clicked = True
        notification.clicked_at = timezone.now()
        notification.save()
        return Response({'status': 'marked as clicked'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Marquer toutes les notifications comme lues"""
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(is_read=True, read_at=timezone.now())
        return Response({'status': 'all marked as read'})
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archiver une notification"""
        notification = self.get_object()
        notification.is_archived = True
        notification.save()
        return Response({'status': 'archived'})
    
    @action(detail=False, methods=['post'])
    def archive_all(self, request):
        """Archiver toutes les notifications"""
        self.get_queryset().update(is_archived=True)
        return Response({'status': 'all archived'})


class NotificationPreferenceViewSet(viewsets.ViewSet):
    """ViewSet pour gérer les préférences de notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def get_preferences(self, request):
        """Récupérer les préférences"""
        try:
            prefs = request.user.notification_preferences
            serializer = NotificationPreferenceSerializer(prefs)
            return Response(serializer.data)
        except NotificationPreference.DoesNotExist:
            prefs = NotificationPreference.objects.create(user=request.user)
            serializer = NotificationPreferenceSerializer(prefs)
            return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_preferences(self, request):
        """Mettre à jour les préférences"""
        try:
            prefs = request.user.notification_preferences
        except NotificationPreference.DoesNotExist:
            prefs = NotificationPreference.objects.create(user=request.user)
        
        serializer = NotificationPreferenceSerializer(prefs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet pour les notifications programmées"""
    serializer_class = NotificationScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return NotificationSchedule.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
