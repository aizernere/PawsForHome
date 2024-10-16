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