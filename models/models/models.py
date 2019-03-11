from django.db import models
#python ./manage.py makemigrations models && python ./manage.py migrate models && python manage.py loaddata db.json && 
class User(models.Model):
    #Username
    username = models.CharField(max_length =10, default = "username")
    password = models.CharField(max_length = 148, default = "password")

    #User Information
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11)
    profile_url = models.URLField()

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10)  # max allowed is 7.
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=15)
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Ride(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
    )
    passengers = models.ManyToManyField(User)
    destination = models.CharField(max_length=50)
    start = models.CharField(max_length=50)
    # 2008/11/14/1 == 1pm on 11/14/2008
    depart_time = models.CharField(max_length=13)
    seats_offered = models.PositiveSmallIntegerField()  # # of passengers < seats_offered
    price = models.IntegerField() # In USD

class Authenticator(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    authenticator = models.CharField(max_length = 64)
    date_created = models.CharField(max_length=13)


