from django.db import models
from django.contrib.auth.models import User


class Contest(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    default_code = models.TextField(blank=True, null=True)
    testcases = models.BinaryField()
    hidden_code = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    code = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creator_ip = models.CharField(max_length=31, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"
