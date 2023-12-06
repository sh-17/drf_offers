from django.db import models


class Offer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    media_file = models.ImageField(upload_to='api/media/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status']