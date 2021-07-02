from django.db import models

# Create your models here.


class New(models.Model):
    title = models.CharField(max_length=55, blank=True)
    details = models.TextField(blank=True)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
