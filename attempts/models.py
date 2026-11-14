from django.db import models
from students.models import Student
from quizzes.models import Test

# Create your models here.

class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name="attempts", verbose_name="O'quvchi")
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             related_name="attempts", verbose_name="Test")
    score = models.PositiveSmallIntegerField("Ball", default=0)
    started = models.DateTimeField("Boshlangan", auto_now_add=True)
    answers = models.JSONField("Javoblar", default=dict)
    finished = models.BooleanField("Yakunlangan", default=False)

    class Meta:
        verbose_name_plural = "Urinishlar"
        unique_together = ("student", "test")

    def __str__(self):
        return f"{self.student} - {self.test} - {self.score}"