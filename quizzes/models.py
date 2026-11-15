from django.db import models
from subjects.models import Subject
from teachers.models import Teacher
from django.utils import timezone

# Create your models here.
class Test(models.Model):
    title = models.CharField("Sarlavha", max_length=100)
    subject = models.ManyToManyField(Subject, related_name="tests", verbose_name="Fan")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True,
                                related_name="teachers", verbose_name="Yaratgan")
    created = models.DateTimeField("Yaratilgan vaqt" ,auto_now_add=True)
    class Meta:
        verbose_name_plural = "Testlar"

    @property
    def deadline(self):
        local = timezone.localtime(self.created)
        return local.replace(hour=20, minute=0, second=0, microsecond=0)
    def is_open(self):
        return timezone.now() < self.deadline
    def __str__(self):
        return self.title


#Quizzes
class Question(models.Model):
    CORRECT_CHOICES = [(1, "1-variant"), (2, "2-variant"), (3, "3-variant"), (4, "4-variant")]
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             related_name="questions", verbose_name="Test")
    text = models.TextField("Savol")
    option1 = models.CharField("1-variant", max_length=200)
    option2 = models.CharField("2-variant", max_length=200)
    option3 = models.CharField("3-variant", max_length=200)
    option4 = models.CharField("4-variant", max_length=200)
    correct = models.PositiveSmallIntegerField("To'g'ri javob", choices=CORRECT_CHOICES)
    class Meta:
        verbose_name_plural = "Savollar"
    def __str__(self):
        return f"{self.text[:30]}..."