from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Course, Video, Document, Quiz, Exercise
from .ai_course_generator import AICourseGenerator
from analytics.models import EmotionData

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'content/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.video_set.all()
    documents = course.document_set.all()
    quizzes = course.quiz_set.all()
    exercises = course.exercise_set.all()
    return render(request, 'content/course_detail.html', {
        'course': course,
        'videos': videos,
        'documents': documents,
        'quizzes': quizzes,
        'exercises': exercises
    })

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'content/quiz_detail.html', {'quiz': quiz})

@login_required
def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'content/exercise_detail.html', {'exercise': exercise})

@login_required
def generate_course(request):
    """Page pour générer un cours avec l'IA"""
    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        difficulty = request.POST.get('difficulty', 'intermediate')
        subject = request.POST.get('subject', 'sociology')
        generation_type = request.POST.get('generation_type', 'manual')
        generate_multiple = request.POST.get('generate_multiple', 'false') == 'true'
        
        try:
            if generation_type == 'emotion':
                # Générer basé sur l'émotion récente
                recent_emotion = EmotionData.objects.filter(user=request.user).order_by('-recorded_at').first()
                if recent_emotion:
                    if generate_multiple:
                        # Générer plusieurs cours dans différentes matières
                        courses = AICourseGenerator.generate_multiple_courses_by_emotion(
                            request.user,
                            recent_emotion.emotion_type,
                            count=3
                        )
                        messages.success(
                            request, 
                            f'{len(courses)} cours générés avec succès basés sur votre émotion "{recent_emotion.get_emotion_type_display()}" dans différentes matières !'
                        )
                        return redirect('course_list')
                    else:
                        course = AICourseGenerator.generate_course_based_on_emotion(
                            request.user,
                            recent_emotion.emotion_type
                        )
                        messages.success(
                            request, 
                            f'Cours généré avec succès basé sur votre émotion "{recent_emotion.get_emotion_type_display()}" !'
                        )
                        return redirect('course_detail', course_id=course.id)
                else:
                    course = AICourseGenerator.generate_course(
                        topic=topic if topic else None,
                        difficulty=difficulty,
                        subject=subject
                    )
                    messages.success(request, 'Cours généré avec succès !')
                    return redirect('course_detail', course_id=course.id)
            elif generation_type == 'profile':
                # Générer basé sur le profil
                course = AICourseGenerator.generate_course_based_on_profile(request.user)
                messages.success(request, f'Cours généré avec succès adapté à votre niveau "{request.user.profile.get_level_display()}" !')
                return redirect('course_detail', course_id=course.id)
            else:
                # Génération manuelle
                course = AICourseGenerator.generate_course(
                    topic=topic if topic else None,
                    difficulty=difficulty,
                    subject=subject
                )
                messages.success(request, 'Cours généré avec succès !')
                return redirect('course_detail', course_id=course.id)
        except Exception as e:
            messages.error(request, f'Erreur lors de la génération du cours: {str(e)}')
    
    # Récupérer l'émotion récente pour suggestion
    recent_emotion = EmotionData.objects.filter(user=request.user).order_by('-recorded_at').first()
    
    return render(request, 'content/generate_course.html', {
        'recent_emotion': recent_emotion,
        'subjects': Course.SUBJECT_CHOICES
    })

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def generate_course_api(request):
    """API pour générer un cours via AJAX"""
    try:
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        difficulty = data.get('difficulty', 'intermediate')
        subject = data.get('subject', 'sociology')
        generation_type = data.get('generation_type', 'manual')
        generate_multiple = data.get('generate_multiple', False)
        
        if generation_type == 'emotion':
            recent_emotion = EmotionData.objects.filter(user=request.user).order_by('-recorded_at').first()
            if recent_emotion:
                if generate_multiple:
                    courses = AICourseGenerator.generate_multiple_courses_by_emotion(
                        request.user,
                        recent_emotion.emotion_type,
                        count=3
                    )
                    return JsonResponse({
                        'success': True,
                        'courses': [{
                            'id': c.id,
                            'title': c.title,
                            'description': c.description,
                            'difficulty': c.get_difficulty_display(),
                            'subject': c.get_subject_display(),
                            'url': f'/content/{c.id}/'
                        } for c in courses],
                        'message': f'{len(courses)} cours générés dans différentes matières !'
                    })
                else:
                    course = AICourseGenerator.generate_course_based_on_emotion(
                        request.user,
                        recent_emotion.emotion_type
                    )
            else:
                course = AICourseGenerator.generate_course(
                    topic=topic if topic else None,
                    difficulty=difficulty,
                    subject=subject
                )
        elif generation_type == 'profile':
            course = AICourseGenerator.generate_course_based_on_profile(request.user)
        else:
            course = AICourseGenerator.generate_course(
                topic=topic if topic else None,
                difficulty=difficulty,
                subject=subject
            )
        
        return JsonResponse({
            'success': True,
            'course': {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'difficulty': course.get_difficulty_display(),
                'subject': course.get_subject_display(),
                'url': f'/content/{course.id}/'
            },
            'message': 'Cours généré avec succès !'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
