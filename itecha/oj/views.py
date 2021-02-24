import requests
from django.conf import settings
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


class LoginView(APIView):
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


def execute_code(code: str, code_input: str = "") -> bytes:
    """Executes Python code and collects its output"""

    import sys
    import traceback
    from io import StringIO

    if not code_input.endswith("\n"):
        code_input += "\n"
    input_buffer = StringIO()
    input_buffer.write(code_input)
    input_buffer.seek(0)
    sys.stdin = input_buffer

    output_buffer = StringIO()
    sys.stdout = output_buffer
    sys.stderr = output_buffer

    try:
        exec(code, {})
    except Exception as e:
        traceback.print_exc()
    output = output_buffer.getvalue().encode()

    # Restore the original stdin and stdout
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    sys.stdout = sys.__stderr__

    return output


class PythonExecutorView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if settings.PYTHON_EXECUTOR:
            requests.post(settings.PYTHON_EXECUTOR, json=request.json)
        else:
            source = request.data.get("source")
            input = request.data.get("input")
            return Response(execute_code(source, input))


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
