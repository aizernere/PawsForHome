from django.db import models
from django.conf import settings

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pets/', default='pets/default_pet.jpg') #test
    type = models.CharField(max_length=100)
    age = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField()
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class AdoptionRequest(models.Model):
    HOUSING_CHOICES = [
        ('Apartment', 'Apartment'),
        ('House', 'House'),
        ('Condominium', 'Condominium'),
        ('Other', 'Other'),
    ]

    HOUSEHOLD_CHOICES = [
        ('Active', 'Active'),
        ('Calm', 'Calm'),
        ('Noisy', 'Noisy'),
        ('Quiet', 'Quiet'),
    ]

    GENERAL_INFO_CHOICES = [
        ('Companion for child', 'Companion for child'),
        ('Companion for other pet', 'Companion for other pet'),
        ('Security', 'Security'),
        ('Service animal', 'Service animal'),
        ('House pet', 'House pet'),
        ('Breeding', 'Breeding'),
        ('Other', 'Other'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    housing_type = models.CharField(max_length=20, choices=HOUSING_CHOICES, default='Apartment')
    household_description = models.CharField(max_length=20, choices=HOUSEHOLD_CHOICES, default='Calm')
    general_info = models.CharField(max_length=50, choices=GENERAL_INFO_CHOICES, default='House pet')
    other_housing_description = models.TextField(blank=True, null=True)
    other_general_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pet.name}"