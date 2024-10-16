from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

Account = get_user_model()  # Reference to the Account model

class Message(models.Model):
    sender = models.ForeignKey(Account, related_name='sent_pmessages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='received_pmessages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'