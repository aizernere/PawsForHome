from django.db import models
from django.conf import settings
from django.utils import timezone
from pmessages.models import Message
from main.models import Notification

# Create your models here.
class Pet(models.Model):
    STATUS_CHOICES = [
        (1, 'Available'),
        (2, 'Adopted'),
    ]
    
    TYPE_CHOICES = [
    ('Dog', 'Dog'),
    ('Cat', 'Cat'),
    ('Bird', 'Bird'),
    ('Fish', 'Fish'),
    ('Rabbit', 'Rabbit'),
    ('Hamster', 'Hamster'),
    ('Guinea Pig', 'Guinea Pig'),
    ('Frog', 'Frog'),
    ('Ferret', 'Ferret'),
    ('Chinchilla', 'Chinchilla'),
    ('Hedgehog', 'Hedgehog'),
    ('Mouse', 'Mouse'),
    ('Rat', 'Rat'),
    ('Turtle', 'Turtle'),
    ('Snake', 'Snake'),
    ('Lizard', 'Lizard'),
    ('Parrot', 'Parrot'),
    ('Canary', 'Canary'),
    ('Budgerigar', 'Budgerigar'),
    ('Cockatoo', 'Cockatoo'),
    ('Macaw', 'Macaw'),
    ('Lovebird', 'Lovebird'),
    ('Quail', 'Quail'),
    ('Duck', 'Duck'),
    ('Chicken', 'Chicken'),
    ('Goat', 'Goat'),
    ('Pig', 'Pig'),
    ('Spider', 'Spider'),
    ('Tarantula', 'Tarantula'),
    ('Other', 'Other'),
    ]


    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pets/', default='pets/default_pet.jpg')
    type = models.CharField(choices=TYPE_CHOICES, max_length=20, default='other')
    age_years = models.IntegerField(default=0)
    age_months = models.IntegerField(default=0)
    description = models.TextField(blank=True,null=True)
    location = models.TextField(blank=True,null=True, default='N/A')
    breed = models.CharField(max_length=50, blank=True, null=True)
    adoption_fee = models.IntegerField(default=0, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1) 
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class AdoptionRequest(models.Model):

    STATUS_CHOICES = [
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    ]

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
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
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
    
    def accept(self):
        self.status = 2
        self.pet.status = 2 
        self.save()
        self.pet.save()
        output = f"Your adoption request for {self.pet.name} has been accepted! Please contact {self.pet.owner.first_name} to arrange the adoption."
        input = f"You have accepted the adoption request for {self.pet.name}! Please contact {self.account.first_name} to arrange the adoption."
        messageoutput = f"Your adoption request for {self.pet.name} has been accepted! Please contact me to arrange the adoption."
        Message.objects.create(
            sender=self.pet.owner,
            receiver=self.account, 
            content=messageoutput,
            timestamp=timezone.now()
        )
        Notification.objects.create(account=self.account, notification=output)
        Notification.objects.create(account=self.pet.owner, notification=input)
    

    def reject(self):
        self.status = 3
        self.save()
        self.pet.save()
        output = f"Your adoption request for {self.pet.name} has been rejected!"
        input = f"You have rejected the adoption request by {self.account.first_name} for {self.pet.name}."
        Message.objects.create(
            sender=self.pet.owner,  
            receiver=self.account, 
            content=output,
            timestamp=timezone.now()
        )
        Notification.objects.create(account=self.account, notification=output)
        Notification.objects.create(account=self.pet.owner, notification=input)

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pet')

    def __str__(self):
        return f"{self.user.email} - {self.pet.name}"