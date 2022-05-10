from django.urls import include, path
from rest_framework import routers

from .views import (
    LoginView,
    LogoutView,
    PythonExecutorView,
    ContestViewSet,
    ProblemViewSet,
    SubmissionViewSet,
    UserViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"contests", ContestViewSet)
router.register(r"problems", ProblemViewSet)
router.register(r"submissions", SubmissionViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("python-executor", PythonExecutorView.as_view()),
    path("", include(router.urls)),
]
