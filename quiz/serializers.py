from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizInvitation, QuizParticipation, QuizAnswer
from django.contrib.auth import get_user_model

User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'creator',
                  'created_at', 'updated_at', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers', [])
            question = Question.objects.create(quiz=quiz, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return quiz


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
