from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Recommendation, EmotionData
from .ai_service import AIRecommendationService, EmotionRecognitionService
from content.models import Course
from accounts.models import Historique

@login_required
def dashboard(request):
    user = request.user
    # Statistiques de l'utilisateur
    total_courses = Course.objects.count()
    completed_courses = Historique.objects.filter(user=user, content_type='course', completed=True).count()
    total_points = user.profile.points
    
    # Générer des recommandations IA si nécessaire
    if not Recommendation.objects.filter(user=user, viewed=False).exists():
        AIRecommendationService.generate_recommendations(user)
    
    # Recommandations
    recommendations = Recommendation.objects.filter(user=user, viewed=False)[:5]
    
    # Données émotionnelles récentes
    recent_emotions = EmotionData.objects.filter(user=user)[:10]
    
    # Analyser l'état d'apprentissage
    learning_state = EmotionRecognitionService.analyze_learning_state(user)
    
    # Progression globale
    progress = (completed_courses / total_courses * 100) if total_courses > 0 else 0
    
    context = {
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'total_points': total_points,
        'recommendations': recommendations,
        'recent_emotions': recent_emotions,
        'progress': progress,
        'learning_state': learning_state,
    }
    return render(request, 'analytics/dashboard.html', context)

@login_required
def recommendations(request):
    # Générer de nouvelles recommandations IA
    AIRecommendationService.generate_recommendations(request.user)
    
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-score')
    return render(request, 'analytics/recommendations.html', {'recommendations': recommendations})

@login_required
def record_emotion(request):
    if request.method == 'POST':
        emotion_type = request.POST.get('emotion_type')
        intensity = float(request.POST.get('intensity', 0.5))
        context = request.POST.get('context', '')
        
        EmotionData.objects.create(
            user=request.user,
            emotion_type=emotion_type,
            intensity=intensity,
            context=context
        )
        
        # Générer des recommandations de cours basées sur l'émotion
        recommended_courses = AIRecommendationService.get_courses_by_emotion(
            request.user, 
            emotion_type, 
            limit=5
        )
        
        if recommended_courses:
            messages.success(
                request, 
                f'Émotion enregistrée ! {len(recommended_courses)} cours recommandés basés sur votre état émotionnel.'
            )
        else:
            messages.success(request, 'Émotion enregistrée avec succès!')
        
        # Rediriger vers les recommandations si des cours sont disponibles
        if recommended_courses:
            return redirect('recommendations')
        return redirect('dashboard')
    return render(request, 'analytics/record_emotion.html')

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def recognize_emotion_api(request):
    """API pour la reconnaissance d'émotion via webcam"""
    try:
        data = json.loads(request.body)
        emotion_type = data.get('emotion_type', 'neutral')
        confidence = float(data.get('confidence', 0.5))
        intensity = float(data.get('intensity', 0.5))
        context = data.get('context', 'Reconnaissance via webcam')
        
        # Enregistrer l'émotion
        emotion = EmotionData.objects.create(
            user=request.user,
            emotion_type=emotion_type,
            intensity=intensity,
            context=context
        )
        
        # Analyser l'état d'apprentissage
        learning_state = EmotionRecognitionService.analyze_learning_state(request.user)
        
        # Générer des recommandations de cours basées sur l'émotion
        recommended_courses = AIRecommendationService.get_courses_by_emotion(
            request.user, 
            emotion_type, 
            limit=5
        )
        
        # Préparer les données des cours pour la réponse JSON
        courses_data = []
        for rec in recommended_courses:
            courses_data.append({
                'id': rec.course.id,
                'title': rec.course.title,
                'description': rec.course.description[:100] + '...' if len(rec.course.description) > 100 else rec.course.description,
                'difficulty': rec.course.get_difficulty_display(),
                'score': rec.score,
                'reason': rec.reason,
                'url': f'/content/{rec.course.id}/'
            })
        
        return JsonResponse({
            'success': True,
            'emotion_id': emotion.id,
            'emotion_type': emotion_type,
            'learning_state': learning_state,
            'recommended_courses': courses_data,
            'message': f'Émotion "{emotion.get_emotion_type_display()}" détectée ! {len(courses_data)} cours recommandés.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def emotion_recognition(request):
    """Page pour la reconnaissance d'émotion en temps réel"""
    return render(request, 'analytics/emotion_recognition.html')

@login_required
def generate_ai_recommendations(request):
    """Génère de nouvelles recommandations IA"""
    recommendations = AIRecommendationService.generate_recommendations(request.user)
    return redirect('recommendations')
