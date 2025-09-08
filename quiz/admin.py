
from django.contrib import admin
from .models import Quiz, Question, Answer, QuizInvitation, QuizParticipation, QuizAnswer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "creator", "created_at")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "text")
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct")


@admin.register(QuizInvitation)
class QuizInvitationAdmin(admin.ModelAdmin):
    list_display = ("quiz", "participant", "invited_at",
                    "accepted", "accepted_at")


@admin.register(QuizParticipation)
class QuizParticipationAdmin(admin.ModelAdmin):
    list_display = ("quiz", "participant", "started_at",
                    "completed_at", "score")


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ("participation", "question", "answer", "answered_at")
