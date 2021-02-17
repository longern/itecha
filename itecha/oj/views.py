from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView, Response
from .authentication import generate_token

from .models import Contest, Problem, Submission
from .serializers import (
    BasicProblemSerializer,
    ContestSerializer,
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
            # login(request, user)
            return Response({"token": generate_token(user)})
        else:
            return Response(status=401)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["GET"], detail=False)
    def current(self, request):
        if not request.user.is_authenticated:
            return Response({}, 200)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ProblemSerializer
        return BasicProblemSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filterset_fields = ["creator", "problem"]

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user, creator_ip=self.request.META.get("REMOTE_ADDR")
        )
