from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )


class Department(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.id) + " " + self.title


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True
    )
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name
