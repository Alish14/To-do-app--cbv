from django.db import models
from django.contrib.auth.models import User

"""
Create model for User Task and ForeignKey To Django default User model
"""
class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    #description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Create your models here.
