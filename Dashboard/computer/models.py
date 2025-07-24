from django.db import models
from django.utils import timezone

class Assignee(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Computer(models.Model):
    serial_number = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=20,
        choices=[('desktop', 'Desktop'), ('laptop', 'Laptop')],
        default='desktop'
    )
    specification = models.TextField(null=True, blank=True)
    components = models.TextField()
    spare = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[('available', 'Available'), ('assigned', 'Assigned')],
        default='available'
    )
    assignee = models.ForeignKey(Assignee, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

class ComputerHistory(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='history')
    assignee = models.ForeignKey(Assignee, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, null=True)  # e.g., "Assigned" or "Returned"
    timestamp = models.DateTimeField(auto_now_add=True, null=True)  # Timestamp for the action

    def __str__(self):
        return f"{self.computer.name} - {self.action} by {self.assignee if self.assignee else 'N/A'}"
