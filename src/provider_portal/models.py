from django.db import models
from django.db.models import Model
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Patient(Model):
    full_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(blank=True)