from django.test import TestCase, Client
from django.urls import reverse
import urllib.request
import urllib.parse
import json
from models.models import User, Vehicle, Ride
from django.core.exceptions import ObjectDoesNotExist


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1)
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2)

    def test_user_get_request_param(self):
        response = self.client.get(reverse('user_result_id', kwargs={'pk':1}))
        self.assertContains(response, 'first_name')

    def test_user_get_request_object(self):
        response = self.client.get(reverse('user_result_id', kwargs={'pk':1}))
        self.assertEqual(response.json()['first_name'], "Jiwon")

    def test_user_post_request(self):
        data = {
            "phone_number": "121283789",
            "first_name": "Hello",
            "profile_url": "www.google.com",
            "last_name": "Kitty"
            }
        response = self.client.post(reverse('user_result_id', kwargs={'pk':3}), data, content_type="application/json")
        self.assertEqual(response.json()['first_name'], "Hello")

    def test_user_put_request(self):
        data = {
            "phone_number": "121283789",
            "first_name": "Joan",
            "profile_url": "www.google.com",
            "last_name": "Smith"
            }
        response = self.client.put(reverse('user_result_id', kwargs={'pk':1}), data, content_type="application/json")
        self.assertEqual(response.json()['first_name'], "Joan")

    def test_user_delete_request(self):
        response = self.client.delete(reverse('user_result_id', kwargs={'pk':1}))
        try: 
            faulty_access = self.client.get(reverse('user_result_id', kwargs={'pk':1}))
        except ObjectDoesNotExist:
            pass

class VehicleTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1)
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2)
        Vehicle.objects.create(license_plate="123ABC", model="Toyota", color="yellow", driver=User.objects.get(pk=1), id=1)

    def test_user_get_request_param(self):
        response = self.client.get(reverse('vehicle_result_id', kwargs={'pk':1}))
        self.assertContains(response, 'color')

    def test_vehicle_get_request(self):
        response = self.client.get(reverse('vehicle_result_id', kwargs={'pk':1}))
        self.assertEqual(response.json()['model'], "Toyota")

    def test_vehicle_get_put(self):
        data = {
            "license_plate": "983XYZ",
            "model": "Ford",
            "color": "Black",
            "driver": 1, 
        }
        response = self.client.put(reverse('vehicle_result_id', kwargs={'pk':1}), data, content_type="application/json")
        self.assertEqual(response.json()['model'], "Ford")

    def test_vehicle_delete_request(self):
        response = self.client.delete(reverse('vehicle_result_id', kwargs={'pk':1}))
        try: 
            faulty_access = self.client.get(reverse('vehicle_result_id', kwargs={'pk':1}))
        except ObjectDoesNotExist:
            pass
    
class RideTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1)
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2)
        User.objects.create(first_name="Angelina", last_name="Jolie", phone_number="98732487", profile_url="www.google.com", id = 3)
        User.objects.create(first_name="Johnny", last_name="Depp", phone_number="878372384", profile_url="www.google.com", id = 4)
        Vehicle.objects.create(license_plate="123ABC", model="Toyota", color="yellow", driver=User.objects.get(pk=1), id=1)
        Ride.objects.create(vehicle=Vehicle.objects.get(pk=1), start="DC", destination="New York", depart_time="02/23/17", seats_offered=3, price=80, id = 1)

    def test_ride_get_request_param(self):
        response = self.client.get(reverse('ride_result_id', kwargs={'pk':1}))
        self.assertContains(response, 'destination')

    def test_create_ride(self):
        data = {
            "vehicle": 1, 
            "destination": "Montana", 
            "start": "Cville", 
            "depart_time": "11/12/14",
            "price": "13", 
            "seats_offered": 4, 
            "id": 2
        }   
        response = self.client.post(reverse('ride_result'), data, content_type="application/json")
        self.assertEqual(response.json()['start'], "Cville")

    def test_get_ride(self):
        response = self.client.get(reverse('ride_result_id', kwargs={'pk':1}))
        self.assertEqual(response.json()['start'], "DC")

    def test_add_passengers_to_ride(self):
        response = self.client.put(reverse('ride_result_uid', kwargs={'pk':1, 'uid':2}))
        self.assertContains(response, "success")

    def test_delete_ride(self):
        response = self.client.delete(reverse('ride_result_id', kwargs={'pk':1}))
        try: 
            faulty_access = self.client.get(reverse('ride_result_id', kwargs={'pk':1}))
        except ObjectDoesNotExist:
            pass

class HelperMethodTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1)
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2)
        User.objects.create(first_name="Angelina", last_name="Jolie", phone_number="98732487", profile_url="www.google.com", id = 3)
        User.objects.create(first_name="Johnny", last_name="Depp", phone_number="878372384", profile_url="www.google.com", id = 4)
        Vehicle.objects.create(license_plate="123ABC", model="Toyota", color="yellow", driver=User.objects.get(pk=1), id=1)
        Vehicle.objects.create(license_plate="ZXY982", model="Ford", color="black", driver=User.objects.get(pk=2), id=2)
        Ride.objects.create(vehicle=Vehicle.objects.get(pk=1), start="DC", destination="New York", depart_time="02/23/17", seats_offered=3, price=80, id = 1)
        Ride.objects.create(vehicle=Vehicle.objects.get(pk=2), start="Cville", destination="Montana", depart_time="12/25/19", seats_offered=4, price=20, id = 2)


    # URL format : 'api/rides/n/<int:n>/date/<str:date>/<int:is_after>'
    def test_getNSoonestRides_param(self):
        response = self.client.get(reverse('getNSoonestRides', kwargs={'n':1, 'date':'2000-02-02-20', 'is_after':0}))
        self.assertContains(response, "depart_time")

    def test_getNSoonestRides(self):
        response = self.client.get(reverse('getNSoonestRides', kwargs={'n':1, 'date':'2000-02-02-20', 'is_after':0}))
        self.assertContains(response, "DC")

    def test_getNSoonestRides_incorrect(self):

    # URL format : 'api/user/driver/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>'
    def test_getDriverRideHistory_param(self):
        response = self.client.get(reverse('getDriverRideHistory', 
                   kwargs={'n':2, 'date':'2000-20-02-10', 'is_after':0, 'pk':1}))
        self.assertContains(response, "depart_time")

    def test_getDriverRideHistory(self):
        response = response = self.client.get(reverse('getDriverRideHistory', 
                   kwargs={'n':2, 'date':'2000-20-02-10', 'is_after':0, 'pk':2}))
        self.assertContains(response, "Cville")

    # URL format : 'api/user/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>'
    def test_getNUserRideHistory_param(self):
        response = self.client.get(reverse('getNUserRideHistory', kwargs={'n':5, 'date':"2000-20-02-10", 'is_after':1, 'pk': 3}))
        self.assertContains(response, "date")
    
    def test_getNUserRideHistory(self):
        response = self.client.get(reverse('getNUserRideHistory', kwargs={'n':2, 'date':"2000-20-02-10", 'is_after':1, 'pk': 3}))
