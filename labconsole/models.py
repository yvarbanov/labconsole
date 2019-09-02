from django.db import models

# Create your models here.

class LabConsole(models.Model):
    token = models.CharField(max_length=32)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    project = models.CharField(max_length=20)
