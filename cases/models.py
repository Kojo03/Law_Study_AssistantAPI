from django.db import models
from books.models import Topic

class Case(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="cases")
    title = models.CharField(max_length=255)
    summary = models.TextField()
    citation = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
