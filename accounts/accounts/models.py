from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class File(models.Model):
    file = models.FileField(upload_to='files')
    file_ext = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self) -> str:
        return self.file.name