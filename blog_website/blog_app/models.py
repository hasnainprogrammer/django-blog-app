from statistics import mode
from django.db import models
from datetime import datetime

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.title