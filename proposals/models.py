from django.db import models


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)


class Task(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    completed = models.BooleanField()
