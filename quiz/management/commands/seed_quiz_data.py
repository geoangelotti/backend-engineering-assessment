from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quiz.models import Quiz, Question, Answer, QuizInvitation

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample quizzes, questions, answers, and users"

    def handle(self, *args, **kwargs):
        # Create users with hashed passwords
        creator, created_creator = User.objects.get_or_create(
            username='creator')
        if created_creator:
            creator.set_password('pass')
            creator.save()
        participant, created_participant = User.objects.get_or_create(
            username='participant')
        if created_participant:
            participant.set_password('pass')
            participant.save()

        # Create a quiz
        quiz, _ = Quiz.objects.get_or_create(
            name='Sample Quiz', description='A sample quiz', creator=creator)
        q1, _ = Question.objects.get_or_create(quiz=quiz, text='What is 2+2?')
        Answer.objects.get_or_create(question=q1, text='3', is_correct=False)
        Answer.objects.get_or_create(question=q1, text='4', is_correct=True)

        q2, _ = Question.objects.get_or_create(
            quiz=quiz, text='What is the capital of France?')
        Answer.objects.get_or_create(
            question=q2, text='Berlin', is_correct=False)
        Answer.objects.get_or_create(
            question=q2, text='Paris', is_correct=True)

        # Invite participant
        QuizInvitation.objects.get_or_create(
            quiz=quiz, participant=participant)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
