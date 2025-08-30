from django.db import models
from django.core.validators import MinValueValidator
from books.models import Topic

class Case(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="cases")
    title = models.CharField(max_length=255)
    suit_number = models.CharField(max_length=100, unique=True)
    number_of_pages = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    summary = models.TextField()
    citation = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    total_copies = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    available_copies = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=1)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New case
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)
    
    @property
    def is_available(self):
        return self.available_copies > 0

    def __str__(self):
        return self.title
