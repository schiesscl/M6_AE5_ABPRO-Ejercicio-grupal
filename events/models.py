from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    EVENT_TYPES = [
        ('conference', 'Conferencia'),
        ('concert', 'Concierto'),
        ('seminar', 'Seminario'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_private = models.BooleanField(default=False)
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    attendees = models.ManyToManyField(
        User,
        related_name='attending_events',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ("manage_event", "Can manage events"),
            ("view_private_event", "Can view private events"),
        ]
    
    def __str__(self):
        # ensure a string is always returned for static type checkers
        return str(self.title)
