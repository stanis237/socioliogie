from rest_framework import serializers
from .models import Exercise, Question, Answer, ExerciseSubmission, QuestionResponse, Quiz

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'order', 'is_correct', 'explanation', 'feedback']


class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'order', 'explanation', 'feedback']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_type', 'text', 'image', 'hints', 'difficulty_score', 'answers']


class ExerciseSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exercise
        fields = ['id', 'lesson', 'title', 'description', 'exercise_type', 'difficulty_level',
                 'instructions', 'points', 'time_limit_minutes', 'learning_objectives', 'adaptive',
                 'questions', 'created_at', 'updated_at']


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ['id', 'question', 'selected_answer', 'text_response', 'code_response',
                 'is_correct', 'score', 'time_spent_seconds', 'attempt_number', 'answered_at']


class ExerciseSubmissionSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source='exercise.title', read_only=True)
    question_responses = QuestionResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = ExerciseSubmission
        fields = ['id', 'exercise', 'exercise_title', 'status', 'started_at', 'submitted_at',
                 'completed_at', 'time_spent_seconds', 'score', 'max_score', 'percentage',
                 'feedback', 'ai_feedback', 'attempts_count', 'question_responses']
        read_only_fields = ['id', 'started_at', 'submitted_at', 'completed_at']


class QuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'title', 'description', 'pass_percentage', 'randomize_questions',
                 'randomize_answers', 'show_answers', 'allow_review', 'max_attempts',
                 'questions_count', 'created_at', 'updated_at']
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'title', 'description', 'pass_percentage', 'randomize_questions',
                 'randomize_answers', 'show_answers', 'allow_review', 'max_attempts',
                 'questions', 'created_at', 'updated_at']
