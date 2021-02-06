from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView, Response

from .models import Problem, Submission
from .serializers import (
    BasicProblemSerializer,
    ProblemSerializer,
    SubmissionSerializer,
    UserSerializer,
)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"token": str(user.id)})
        else:
            raise ValueError()


class CurrentUserView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({}, 200)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ProblemSerializer
        return BasicProblemSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user, creator_ip=self.request.META.get("REMOTE_ADDR")
        )
