import string
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class ClassNumber(models.Model):
    LETTER_CHOICES = [(m, m) for m in string.ascii_uppercase[:7] if m!='C']
    number = models.PositiveSmallIntegerField("Sinf", validators=[MinValueValidator(1), MaxValueValidator(11)])
    letter = models.CharField("Sinf bo'limi", max_length=1, choices=LETTER_CHOICES)
    class Meta:
        verbose_name_plural = "Sinflar"
        unique_together = ("number", "letter")
    def __str__(self):
        return f'{self.number}-"{self.letter}"'


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="students", verbose_name="Akkaunt")
    first_name = models.CharField("Ism", max_length=25)
    last_name = models.CharField("Familiya", max_length=25)
    grade = models.ForeignKey(ClassNumber, on_delete=models.SET_NULL, null=True, related_name="students")
    class Meta:
        verbose_name_plural = "O'quvchilar"
    def __str__(self):
        return f"{self.last_name} {self.first_name}({self.grade})"