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
from accounts.models import Historique


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'content/course_list.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # --- Premium Content Locking ---
    if course.difficulty in ['intermediate', 'advanced'] and not request.user.profile.is_premium:
        messages.warning(
            request,
            "Ce cours de niveau intermédiaire/avancé est réservé aux membres Premium. "
            "Abonnez-vous pour y accéder."
        )
        return redirect('pricing')

    videos = course.video_set.all()
    documents = course.document_set.all()
    quizzes = course.quiz_set.all()
    exercises = course.exercise_set.all()

    # Statut de complétion depuis l'historique
    historique_entry = Historique.objects.filter(
        user=request.user, content_type='course', content_id=course.id
    ).first()
    is_completed = historique_entry.completed if historique_entry else False

    return render(request, 'content/course_detail.html', {
        'course': course,
        'videos': videos,
        'documents': documents,
        'quizzes': quizzes,
        'exercises': exercises,
        'is_completed': is_completed,
    })


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Premium locking via parent course
    if quiz.course.difficulty in ['intermediate', 'advanced'] and not request.user.profile.is_premium:
        messages.warning(request, "Ce quiz appartient à un cours réservé aux membres Premium.")
        return redirect('pricing')

    return render(request, 'content/quiz_detail.html', {'quiz': quiz})


@login_required
def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    # Premium locking via parent course
    if exercise.course.difficulty in ['intermediate', 'advanced'] and not request.user.profile.is_premium:
        messages.warning(request, "Cet exercice appartient à un cours réservé aux membres Premium.")
        return redirect('pricing')

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

        # --- Restriction gratuit : 1 génération max / niveau débutant seulement ---
        profile = request.user.profile
        if not profile.is_premium:
            has_generated = Historique.objects.filter(
                user=request.user, content_type='course'
            ).exists()
            if has_generated:
                messages.error(
                    request,
                    "Les comptes gratuits sont limités à 1 cours généré par l'IA. "
                    "Passez Premium pour des générations illimitées !"
                )
                return redirect('pricing')
            # Forcer les paramètres gratuits
            difficulty = 'beginner'
            generate_multiple = False
            generation_type = 'manual'

        try:
            if generation_type == 'emotion':
                recent_emotion = EmotionData.objects.filter(
                    user=request.user
                ).order_by('-recorded_at').first()

                if recent_emotion:
                    if generate_multiple:
                        courses = AICourseGenerator.generate_multiple_courses_by_emotion(
                            request.user, recent_emotion.emotion_type, count=3
                        )
                        for c in courses:
                            Historique.objects.get_or_create(
                                user=request.user,
                                content_type='course',
                                content_id=c.id,
                                defaults={'progress': 0, 'completed': False},
                            )
                        messages.success(
                            request,
                            f'{len(courses)} cours générés selon votre émotion "{recent_emotion.get_emotion_type_display()}" !'
                        )
                        return redirect('course_list')
                    else:
                        course = AICourseGenerator.generate_course_based_on_emotion(
                            request.user, recent_emotion.emotion_type
                        )
                        Historique.objects.get_or_create(
                            user=request.user,
                            content_type='course',
                            content_id=course.id,
                            defaults={'progress': 0, 'completed': False},
                        )
                        messages.success(request, 'Cours généré selon votre émotion !')
                        return redirect('course_detail', course_id=course.id)
                else:
                    course = AICourseGenerator.generate_course(
                        topic=topic or None, difficulty=difficulty, subject=subject
                    )
                    Historique.objects.get_or_create(
                        user=request.user,
                        content_type='course',
                        content_id=course.id,
                        defaults={'progress': 0, 'completed': False},
                    )
                    messages.success(request, 'Cours généré avec succès !')
                    return redirect('course_detail', course_id=course.id)

            elif generation_type == 'profile':
                course = AICourseGenerator.generate_course_based_on_profile(request.user)
                Historique.objects.get_or_create(
                    user=request.user,
                    content_type='course',
                    content_id=course.id,
                    defaults={'progress': 0, 'completed': False},
                )
                messages.success(request, f'Cours généré adapté à votre niveau !')
                return redirect('course_detail', course_id=course.id)

            else:
                course = AICourseGenerator.generate_course(
                    topic=topic or None, difficulty=difficulty, subject=subject
                )
                Historique.objects.get_or_create(
                    user=request.user,
                    content_type='course',
                    content_id=course.id,
                    defaults={'progress': 0, 'completed': False},
                )
                messages.success(request, 'Cours généré avec succès !')
                return redirect('course_detail', course_id=course.id)

        except Exception as e:
            messages.error(request, f'Erreur lors de la génération du cours : {str(e)}')

    recent_emotion = EmotionData.objects.filter(
        user=request.user
    ).order_by('-recorded_at').first()

    return render(request, 'content/generate_course.html', {
        'recent_emotion': recent_emotion,
        'subjects': Course.SUBJECT_CHOICES,
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

        # --- Restriction gratuit ---
        profile = request.user.profile
        if not profile.is_premium:
            has_generated = Historique.objects.filter(
                user=request.user, content_type='course'
            ).exists()
            if has_generated:
                return JsonResponse({
                    'success': False,
                    'error': "Limite atteinte. Les membres gratuits ne peuvent générer qu'un seul cours IA.",
                }, status=403)
            difficulty = 'beginner'
            generate_multiple = False
            generation_type = 'manual'

        course = None
        if generation_type == 'emotion':
            recent_emotion = EmotionData.objects.filter(
                user=request.user
            ).order_by('-recorded_at').first()
            if recent_emotion:
                if generate_multiple:
                    courses = AICourseGenerator.generate_multiple_courses_by_emotion(
                        request.user, recent_emotion.emotion_type, count=3
                    )
                    for c in courses:
                        Historique.objects.get_or_create(
                            user=request.user,
                            content_type='course',
                            content_id=c.id,
                            defaults={'progress': 0, 'completed': False},
                        )
                    return JsonResponse({
                        'success': True,
                        'courses': [{
                            'id': c.id,
                            'title': c.title,
                            'description': c.description,
                            'difficulty': c.get_difficulty_display(),
                            'subject': c.get_subject_display(),
                            'url': f'/content/{c.id}/',
                        } for c in courses],
                        'message': f'{len(courses)} cours générés dans différentes matières !',
                    })
                else:
                    course = AICourseGenerator.generate_course_based_on_emotion(
                        request.user, recent_emotion.emotion_type
                    )
            else:
                course = AICourseGenerator.generate_course(
                    topic=topic or None, difficulty=difficulty, subject=subject
                )
        elif generation_type == 'profile':
            course = AICourseGenerator.generate_course_based_on_profile(request.user)
        else:
            course = AICourseGenerator.generate_course(
                topic=topic or None, difficulty=difficulty, subject=subject
            )

        if course:
            Historique.objects.get_or_create(
                user=request.user,
                content_type='course',
                content_id=course.id,
                defaults={'progress': 0, 'completed': False},
            )
            return JsonResponse({
                'success': True,
                'course': {
                    'id': course.id,
                    'title': course.title,
                    'description': course.description,
                    'difficulty': course.get_difficulty_display(),
                    'subject': course.get_subject_display(),
                    'url': f'/content/{course.id}/',
                },
                'message': 'Cours généré avec succès !',
            })
        return JsonResponse({'success': False, 'error': 'Cours non généré.'}, status=400)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def complete_course(request, course_id):
    """Marque un cours comme complété à 100% et attribue des points."""
    course = get_object_or_404(Course, id=course_id)

    historique, created = Historique.objects.get_or_create(
        user=request.user,
        content_type='course',
        content_id=course.id,
        defaults={'progress': 100, 'completed': True},
    )

    if created or not historique.completed:
        if not created:
            historique.progress = 100
            historique.completed = True
            historique.save()

        profile = request.user.profile
        profile.points += 100
        profile.save()
        messages.success(
            request,
            f"Félicitations ! Vous avez terminé '{course.title}' et gagné 100 points !"
        )
    else:
        messages.info(request, "Vous avez déjà complété ce cours.")

    return redirect('course_detail', course_id=course.id)


@login_required
def generate_certificate(request, course_id):
    """Génère le certificat imprimable (membres Premium uniquement)."""
    course = get_object_or_404(Course, id=course_id)

    if not request.user.profile.is_premium:
        messages.warning(request, "Les certificats sont réservés aux membres Premium.")
        return redirect('pricing')

    historique = Historique.objects.filter(
        user=request.user,
        content_type='course',
        content_id=course.id,
        completed=True,
    ).first()

    if not historique:
        messages.error(
            request,
            "Vous devez d'abord compléter ce cours pour obtenir le certificat."
        )
        return redirect('course_detail', course_id=course.id)

    from django.utils import timezone
    return render(request, 'content/certificate.html', {
        'course': course,
        'date_completed': historique.last_accessed or timezone.now(),
    })


@login_required
@csrf_exempt
def ai_tutor(request):
    """Chatbot Tuteur IA — GET: interface, POST: réponse JSON."""
    from .gemini_service import GeminiService
    from django.utils import timezone

    profile = request.user.profile

    # Réinitialisation journalière du compteur pour les gratuits
    today = timezone.now().date()
    if profile.last_question_reset != today:
        profile.ai_questions_asked_today = 0
        profile.last_question_reset = today
        profile.save()

    questions_left = max(0, 3 - profile.ai_questions_asked_today)

    if request.method == 'POST':
        # Vérifier la limite gratuite
        if not profile.is_premium and questions_left <= 0:
            return JsonResponse({
                'success': False,
                'error': "Limite journalière gratuite atteinte (3 questions/jour). Passez Premium pour continuer.",
            }, status=403)

        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            if not question:
                return JsonResponse({'success': False, 'error': "La question est vide."}, status=400)

            # Incrémenter compteur pour les gratuits
            if not profile.is_premium:
                profile.ai_questions_asked_today += 1
                profile.save()
                questions_left = max(0, 3 - profile.ai_questions_asked_today)

            answer = GeminiService.get_tutor_response(request.user, question)

            return JsonResponse({
                'success': True,
                'answer': answer,
                'questions_left': questions_left if not profile.is_premium else None,
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # GET — afficher l'interface du tuteur
    return render(request, 'content/ai_tutor.html', {
        'is_premium': profile.is_premium,
        'questions_left': questions_left,
    })
