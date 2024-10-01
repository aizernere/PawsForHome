from django.db import models

# Create your models here.
class Account(models.Model):
    account_type = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=100)
    password = models.TextField()
    