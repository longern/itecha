import json
import pickle

from django.contrib.auth.models import User
from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers

from .models import Contest, Problem, Submission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "groups", "user_permissions")


class JSONField(serializers.Field):
    def to_representation(self, value):
        try:
            return json.loads(value)
        except EOFError:
            return None

    def to_internal_value(self, data):
        return json.dumps(data, ensure_ascii=False)


class PickleField(serializers.Field):
    def to_representation(self, value):
        try:
            return pickle.loads(value)
        except EOFError:
            return None

    def to_internal_value(self, data):
        return pickle.dumps(data)


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = "__all__"


class ProblemSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    testcases = PickleField()
    tags = JSONField()
    contest = ContestSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = "__all__"


class BasicProblemSerializer(ProblemSerializer):
    class Meta:
        model = Problem
        fields = ["id", "title", "content", "tags"]


class SubmissionSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    problem = ProblemSerializer(read_only=True)
    problem_id = serializers.PrimaryKeyRelatedField(
        queryset=Problem.objects.all(), source="problem", write_only=True
    )

    class Meta:
        model = Submission
        fields = "__all__"
