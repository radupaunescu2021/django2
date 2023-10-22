
from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(default=0)  # 0 for no limit

    TYPE_CHOICES = [
        ('SPORT', 'Sport'),
        ('MUSIC', 'Music'),
        ('POLITICS', 'Politics'),
    ]
    type = models.CharField(
        max_length=10,  # Choose a length that suits your needs
        choices=TYPE_CHOICES,
        default='SPORT',  # Optionally provide a default
    )

    def is_full(self):
        return self.registration_set.count() >= self.capacity if self.capacity > 0 else False

    def __str__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.event.is_full():
            raise ValidationError('The event has reached its maximum capacity.')
        super().save(*args, **kwargs)