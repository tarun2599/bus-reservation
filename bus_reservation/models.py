from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models

class Bus(models.Model):
    company_name = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=50, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    frequency = models.JSONField()  # Example: ["Monday", "Wednesday", "Friday"]
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.bus_number}"

class Reservation(models.Model):
    user_name = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="reservations")
    date = models.DateField()
    seats_reserved = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.user_name} on {self.date} ({self.seats_reserved} seats)"
    
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.full_name
