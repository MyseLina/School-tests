from django.db import models
from students.models import ClassNumber
from teachers.models import Teacher

# Create your models here.
class Subject(models.Model):
    name = models.CharField("Fan nomi", max_length=35)
    grade = models.ForeignKey(ClassNumber, on_delete=models.CASCADE,
                              related_name="subjects", verbose_name="Fan sinfi")
    teacher = models.ManyToManyField(Teacher, related_name="subjects",
                                     verbose_name="O'qituvchilar")
    class Meta:
        verbose_name_plural = "Fanlar"
        unique_together = ("name", "grade")
    def __str__(self):
        return f"{self.name}({self.grade})"