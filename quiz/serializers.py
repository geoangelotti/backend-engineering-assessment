from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizInvitation, QuizParticipation, QuizAnswer
from django.contrib.auth import get_user_model

User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    creator = serializers.StringRelatedField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'creator',
                  'created_at', 'updated_at', 'questions']


class QuizInvitationSerializer(serializers.ModelSerializer):
    quiz = serializers.StringRelatedField()
    participant = serializers.StringRelatedField()

    class Meta:
        model = QuizInvitation
        fields = ['id', 'quiz', 'participant',
                  'invited_at', 'accepted', 'accepted_at']


class QuizParticipationSerializer(serializers.ModelSerializer):
    quiz = serializers.StringRelatedField()
    participant = serializers.StringRelatedField()

    class Meta:
        model = QuizParticipation
        fields = ['id', 'quiz', 'participant',
                  'started_at', 'completed_at', 'score']


class QuizAnswerSerializer(serializers.ModelSerializer):
    participation = serializers.StringRelatedField()
    question = serializers.StringRelatedField()
    answer = serializers.StringRelatedField()

    class Meta:
        model = QuizAnswer
        fields = ['id', 'participation', 'question', 'answer', 'answered_at']
