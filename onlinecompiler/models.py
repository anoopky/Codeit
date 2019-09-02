from django.contrib.auth.models import User
from django.db import models


class Questions(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    input_public = models.TextField()
    output_public = models.TextField()
    explanation = models.TextField()
    verification = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class TestCases(models.Model):
    questionId = models.ForeignKey(Questions, on_delete=models.CASCADE)
    input_private = models.TextField()
    output_private = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.TextField()
    score = models.TextField()
    execution_time = models.TextField()
    status = models.TextField()
    questionId = models.ForeignKey(Questions, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('execution_time', 'score')
        unique_together = ('user', 'questionId',)
