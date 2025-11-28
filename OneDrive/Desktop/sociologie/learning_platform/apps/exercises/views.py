from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Exercise, ExerciseSubmission, Quiz, QuestionResponse
from .serializers import (
    ExerciseSerializer, ExerciseSubmissionSerializer, QuizSerializer,
    QuizDetailSerializer, QuestionResponseSerializer
)

class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les exercices"""
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            return Exercise.objects.filter(lesson_id=lesson_id)
        return Exercise.objects.all()


class ExerciseSubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet pour soumettre et consulter les soumissions d'exercices"""
    serializer_class = ExerciseSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExerciseSubmission.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def start_exercise(self, request):
        """Commencer un exercice"""
        exercise_id = request.data.get('exercise_id')
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            
            # Vérifier les tentatives précédentes
            submissions = ExerciseSubmission.objects.filter(
                user=request.user,
                exercise=exercise,
                status='submitted'
            )
            
            if exercise.time_limit_minutes:
                max_attempts = 1  # Single attempt with time limit
            else:
                max_attempts = 5  # Multiple attempts
            
            if submissions.count() >= max_attempts:
                return Response(
                    {'error': 'Nombre maximum de tentatives atteint'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer une nouvelle soumission
            submission = ExerciseSubmission.objects.create(
                user=request.user,
                exercise=exercise,
                max_score=len(exercise.questions.all()) * exercise.points,
                status='pending'
            )
            
            serializer = self.get_serializer(submission)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exercise.DoesNotExist:
            return Response({'error': 'Exercice non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """Soumettre une réponse à une question"""
        submission = self.get_object()
        question_id = request.data.get('question_id')
        answer_id = request.data.get('answer_id')
        text_response = request.data.get('text_response', '')
        
        try:
            from .models import Question, Answer
            question = Question.objects.get(id=question_id)
            
            answer = None
            if answer_id:
                answer = Answer.objects.get(id=answer_id)
            
            # Créer la réponse
            response = QuestionResponse.objects.create(
                submission=submission,
                question=question,
                selected_answer=answer,
                text_response=text_response
            )
            
            # Vérifier si correcte
            if answer and answer.is_correct:
                response.is_correct = True
                response.score = question.exercise.points
            elif not answer and text_response:
                # Pour les réponses texte, utiliser l'IA pour la vérification
                response.is_correct = None  # À déterminer par l'IA
            
            response.save()
            
            serializer = QuestionResponseSerializer(response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def submit_exercise(self, request, pk=None):
        """Soumettre l'exercice complété"""
        submission = self.get_object()
        
        # Calculer le score
        responses = QuestionResponse.objects.filter(submission=submission)
        total_score = 0
        
        for response in responses:
            if response.is_correct:
                total_score += response.score or 0
        
        submission.status = 'submitted'
        submission.submitted_at = timezone.now()
        submission.score = total_score
        submission.percentage = (total_score / submission.max_score * 100) if submission.max_score > 0 else 0
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les quiz"""
    queryset = Quiz.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizSerializer
    
    def get_queryset(self):
        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            return Quiz.objects.filter(lesson_id=lesson_id)
        return Quiz.objects.all()
