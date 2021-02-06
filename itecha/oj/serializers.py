import pickle

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Problem, Submission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PickleField(serializers.Field):
    def to_representation(self, value):
        try:
            return pickle.loads(value)
        except EOFError:
            return None

    def to_internal_value(self, data):
        return pickle.dumps(data)


class ProblemSerializer(serializers.ModelSerializer):
    testcases = PickleField()

    class Meta:
        model = Problem
        fields = "__all__"


class BasicProblemSerializer(ProblemSerializer):
    class Meta:
        model = Problem
        fields = ["id", "title", "content", "default_code"]


class SubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(read_only=True)
    problem_id = serializers.PrimaryKeyRelatedField(
        queryset=Problem.objects.all(), source="problem", write_only=True
    )

    class Meta:
        model = Submission
        fields = "__all__"
        depth = 1
