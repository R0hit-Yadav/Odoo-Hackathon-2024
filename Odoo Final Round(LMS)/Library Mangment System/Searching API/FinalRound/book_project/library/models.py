from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)  # Ensure this is set to be a number
    isbn = models.CharField(max_length=13, unique=True, null=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # Add default or null=True if needed

    def __str__(self):
        return self.title



