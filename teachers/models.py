from django.db import models
from django.conf import settings

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="teachers", verbose_name="Akkaunt")
    first_name = models.CharField("Ism", max_length=25)
    last_name = models.CharField("Familiya", max_length=25)
    class Meta:
        verbose_name_plural = "O'qituvchilar"
    def __str__(self):
        return f"{self.last_name} {self.first_name}"