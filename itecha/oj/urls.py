from django.urls import include, path
from rest_framework import routers

from .views import (
    Login,
    ProblemViewSet,
    SubmissionViewSet,
    UserViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"problems", ProblemViewSet)
router.register(r"submissions", SubmissionViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("login", Login.as_view()),
    path("", include(router.urls)),
]
