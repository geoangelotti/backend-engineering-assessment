from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuizParticipationViewSet, QuizInvitationViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'participations', QuizParticipationViewSet,
                basename='participation')
router.register(r'invitations', QuizInvitationViewSet, basename='invitation')

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version='v1',
        description="API documentation for Quiz as a Service",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
]
