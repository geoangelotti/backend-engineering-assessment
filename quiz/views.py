
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Quiz, Question, Answer, QuizInvitation, QuizParticipation, QuizAnswer
from django.contrib.auth import get_user_model

from .serializers import (
    QuizSerializer, QuestionSerializer, AnswerSerializer,
    QuizInvitationSerializer, QuizParticipationSerializer, QuizAnswerSerializer
)
from django.utils import timezone

User = get_user_model()


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Show quizzes relevant to user (creator or invited/participating)
        return Quiz.objects.filter(
            Q(creator=user) |
            Q(invitations__participant=user) |
            Q(participations__participant=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['get'], url_path='progress')
    def progress(self, request, pk=None):
        quiz = self.get_object()
        participations = quiz.participations.all()
        return Response({
            'quiz': quiz.name,
            'participants': [
                        {
                            'user': p.participant.username,
                            'score': p.score,
                            'completed_at': p.completed_at
                        } for p in participations
                        ]
        })

    @action(detail=True, methods=['get'], url_path='scores')
    def scores(self, request, pk=None):
        quiz = self.get_object()
        scores = quiz.participations.values('participant__username', 'score')
        return Response(list(scores))


class QuizParticipationViewSet(viewsets.ModelViewSet):
    serializer_class = QuizParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QuizParticipation.objects.filter(participant=user)

    @action(detail=True, methods=['get'], url_path='progress')
    def progress(self, request, pk=None):
        participation = self.get_object()
        answers = participation.answers.all()
        return Response({
            'quiz': participation.quiz.name,
            'answered_questions': answers.count(),
            'score': participation.score,
            'completed_at': participation.completed_at
        })


class QuizInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = QuizInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QuizInvitation.objects.filter(participant=user)

    @action(detail=True, methods=['post'], url_path='accept')
    def accept(self, request, pk=None):
        invitation = self.get_object()
        if not invitation.accepted:
            invitation.accepted = True
            invitation.accepted_at = timezone.now()
            invitation.save()
        return Response({'accepted': invitation.accepted, 'accepted_at': invitation.accepted_at})
