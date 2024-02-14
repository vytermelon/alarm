from django.db import models

# Create your models here.
from django.db import models


class Question(models.Model):
    def __str__(self):
        return self.question_text
    question_text = models.TextField()
    answer_text = models.TextField(default="N/A")
    day = models.DateTimeField()
    complete = models.BooleanField(default=False)


class Verify(models.Model):
    complete = models.BooleanField(default=False)

