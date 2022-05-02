from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Exam(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    start_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = (
        (1, _("Multiple choices")),
        (2, _("Fill-in-the-blank")),
    )

    text = models.TextField()
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.IntegerField(choices=QUESTION_TYPES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
