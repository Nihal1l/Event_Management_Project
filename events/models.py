from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,default=1, related_name='events_category')
    participants = models.ManyToManyField(User, related_name='events_participants')
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="PENDING")
    def __str__(self):
        return self.name

class EventDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    event = models.OneToOneField(
        Event,
        on_delete=models.DO_NOTHING,
        related_name='details',
    )
    asset = models.ImageField(upload_to='events_asset',  blank=True, null=True,
                              default="events_asset/default_img.jpg")
    priority = models.CharField(
        max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details form Event {self.event.name}"

 

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name