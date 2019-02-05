from django.db import models
# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length = 11)
    profile_url = models.URLField()
class Vehicle(models.Model):
    license_plate = models.CharField(max_length = 10 ) # max allowed is 7.
    model = models.CharField(max_length = 20)
    color = models.CharField(max_length = 15)
    capacity = models.PositiveSmallIntegerField() # needs to be checked for zero
    driver = models.ForeignKey(User, on_delete = models.CASCADE)