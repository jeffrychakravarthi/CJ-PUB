from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensures single response per user
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)