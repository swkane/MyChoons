from django.db import models

class Track(models.Model):
  CHOICES = [
    ('SC', 'SoundCloud')
  ]

  provider = models.CharField(max_length=2, choices=CHOICES)
  provider_id = models.CharField(max_length=100, blank=True)
  uploaded = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)