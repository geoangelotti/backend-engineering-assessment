
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Quiz, Question, Answer, QuizInvitation, QuizParticipation
from rest_framework.test import APIClient

User = get_user_model()


class QuizModelTest(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(
            username='creator', password='pass')
        self.participant = User.objects.create_user(
            username='participant', password='pass')
        self.quiz = Quiz.objects.create(
            name='Test Quiz', description='A test quiz', creator=self.creator)
        self.question = Question.objects.create(
            quiz=self.quiz, text='What is 2+2?')
        self.answer1 = Answer.objects.create(
            question=self.question, text='3', is_correct=False)
        self.answer2 = Answer.objects.create(
            question=self.question, text='4', is_correct=True)
        self.invitation = QuizInvitation.objects.create(
            quiz=self.quiz, participant=self.participant)

    def test_quiz_creation(self):
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(self.quiz.questions.count(), 1)
        self.assertEqual(self.question.answers.count(), 2)

    def test_invitation_acceptance(self):
        self.invitation.accepted = True
        self.invitation.save()
        self.assertTrue(self.invitation.accepted)

    def test_participation(self):
        participation = QuizParticipation.objects.create(
            quiz=self.quiz, participant=self.participant, score=1)
        self.assertEqual(participation.score, 1)


class QuizAPITest(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(
            username='creator', password='pass')
        self.participant = User.objects.create_user(
            username='participant', password='pass')
        self.quiz = Quiz.objects.create(
            name='API Quiz', description='API test quiz', creator=self.creator)
        self.client = APIClient()
        self.client.force_authenticate(user=self.creator)

    def test_quiz_list(self):
        response = self.client.get('/api/quizzes/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)
