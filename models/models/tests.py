from django.test import TestCase, Client
from django.urls import reverse
import urllib.request
import urllib.parse
import json
import datetime
from models.models import User, Vehicle, Ride
from models.views import *
from django.core.exceptions import ObjectDoesNotExist


#
#TODO: UPDATE CHANGES / REMOVE USER-RESULT
#


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1, username="jiwonC", password="hello")
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2, username="pabloR", password="password")

    def test_user_post_request(self):
        data = {
            "phone_number": "121283789",
            "first_name": "Hello",
            "profile_url": "www.google.com",
            "last_name": "Kitty", 
            "password": "pw",
            "username": "kittyH"
            }
        response = self.client.post(reverse('user_result_id', kwargs={'pk':3}), data, content_type="application/json")
        self.assertEqual(response.json()['first_name'], "Hello")

    def test_user_put_request(self):
        data = {
            "phone_number": "121283789",
            "first_name": "Joan",
            "profile_url": "www.google.com",
            "last_name": "Smith", 
            "username": "JoanS",
            "password": "pwd"
            }
        response = self.client.put(reverse('user_result_id', kwargs={'pk':1}), data, content_type="application/json")
        self.assertEqual(response.json()['first_name'], "Joan")

    def test_user_delete_request(self):
        response = self.client.delete(reverse('user_result_id', kwargs={'pk':1}))
        self.assertContains(response, "key")

class VehicleTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1, username="jiwonC", password="hello")
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2, username="pabloR", password="password")
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
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1, username="jiwonC", password="hello")
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2, username="pabloR", password="password")
        User.objects.create(first_name="Angelina", last_name="Jolie", phone_number="98732487", profile_url="www.google.com", id = 3, username="angelinaG", password="angpwd")
        User.objects.create(first_name="Johnny", last_name="Depp", phone_number="878372384", profile_url="www.google.com", id = 4, username="johnnyD", password="jonpwd")
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
        response = self.client.post(reverse('ride_result_id', kwargs={'pk':1}), data, content_type="application/json")
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
    def test_convertTime_am(self):
        test_date = "2020/20/02/10"
        self.assertEquals(convertTime(test_date), "10am")

    def test_convertTime_pm(self):
        test_date = "2020/20/02/22"
        self.assertEquals(convertTime(test_date), "10pm")

    # Format: YYYY/DD/MM to MM/DD/YYYY
    def test_convertToDate(self):
        test_date = "2020/20/02/10"
        self.assertEquals(convertToDate(test_date), "02/20/2020")

    # returns true if time is greater or equal
    # Format is YYYY-MM-DD as strings
    # def compareTime(old_time, new_time):
    def test_compareTime(self):
        older_time = "2017-01-30"
        later_time = "2018-12-30"
        self.assertTrue(compareTime(older_time, later_time))

class QueryMethodTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name="Jiwon", last_name="Cha", phone_number="1209381092", profile_url="www.google.com", id = 1, username="jiwonC", password="hello")
        User.objects.create(first_name="Pablo", last_name="Ramos", phone_number="12381274", profile_url="www.google.com", id = 2, username="pabloR", password="password")
        User.objects.create(first_name="Angelina", last_name="Jolie", phone_number="98732487", profile_url="www.google.com", id = 3, username="angelinaG", password="angpwd")
        User.objects.create(first_name="Johnny", last_name="Depp", phone_number="878372384", profile_url="www.google.com", id = 4, username="johnnyD", password="jonpwd")
        Vehicle.objects.create(license_plate="123ABC", model="Toyota", color="yellow", driver=User.objects.get(pk=1), id=1)
        Vehicle.objects.create(license_plate="ZXY982", model="Ford", color="black", driver=User.objects.get(pk=2), id=2)
        Ride.objects.create(vehicle=Vehicle.objects.get(pk=1), start="DC", destination="New York", depart_time="2023/11/10/12", seats_offered=3, price=80, id = 1)
        Ride.objects.create(vehicle=Vehicle.objects.get(pk=2), start="Cville", destination="Montana", depart_time="2012/05/05/05", seats_offered=4, price=20, id = 2)

    # Check if the function actually returns a dict type
    def test_convertRidesToDict_type(self):
        all_rides = Ride.objects.all()
        converted = convertRidesToDict(all_rides, 1)
        self.assertIs(type(converted), dict)

    # Check if all rides information is displayed (there are two rides in the database after setUp)
    def test_convertRidesToDict(self):
        all_rides = Ride.objects.all()
        converted = convertRidesToDict(all_rides, 1)
        ride1_start = converted['rides'][0]['start']
        ride2_start = converted['rides'][1]['start']
        self.assertEquals(ride1_start, 'DC')
        self.assertEquals(ride2_start, 'Cville')

    # User with user_id : Pablo
    def test_createAuthenticator(self):
        response = self.client.post(reverse('createauthenticator', kwargs={'user_id':2}))
        json_data = response.json()
        user_info = User.objects.get(pk=json_data['id'])
        # Check that this person is indeed "Pablo"
        self.assertEquals(user_info.first_name, "Pablo")
        # Check if the response returned the authenticator (not error)
        self.assertContains(response, "authenticator")
    
    def test_cookiecheck(self):
        response = self.client.post(reverse('createauthenticator', kwargs={'user_id':1}))
        json_data = response.json()
        authen = json_data['authenticator']
        cookie_resp = self.client.get(reverse('checkcookie', kwargs={'auth_str': authen}))
        self.assertContains(cookie_resp, "valid")
    
    # api/user/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>
    def test_getNUserRideHistory_empty(self):
        Ride.objects.filter(pk=1).update()
        resp = self.client.put(reverse('ride_result_uid', kwargs={'pk':1, 'uid':2}))
        func_resp = self.client.get(reverse('getNUserRideHistory', kwargs={'pk': 2, 'n': 2, 'date':"2000-00-00", 'is_after':0}))
        data = json.loads(json.dumps(func_resp.json()))
        num_items = len(data['rides'])
        self.assertEquals(num_items, 0)
    
    def test_getNUserRideHistory(self):
        Ride.objects.filter(pk=1).update()
        resp = self.client.put(reverse('ride_result_uid', kwargs={'pk':1, 'uid':2}))
        func_resp = self.client.get(reverse('getNUserRideHistory', kwargs={'pk': 2, 'n': 2, 'date':"2000-00-00", 'is_after':1}))
        self.assertContains(func_resp, 'DC')

    # api/rides/n/<int:n>/date/<str:date>/<int:is_after>
    # There is a total of two rides and it gets 2 rides, therefore the length of json result must be 2
    def test_getNSoonestRides(self):
        func_resp = self.client.get(reverse('getNSoonestRides', kwargs={'n': 2, 'date':"2000-00-00", 'is_after':1}))
        data = json.loads(json.dumps(func_resp.json()))
        num_items = len(data['rides'])
        self.assertEquals(num_items, 2)

    def test_getNSoonestRides_empty(self):
        func_resp = self.client.get(reverse('getNSoonestRides', kwargs={'n': 2, 'date':"2000-00-00", 'is_after':0}))
        data = json.loads(json.dumps(func_resp.json()))
        num_items = len(data['rides'])
        self.assertEquals(num_items, 0)
    
    # api/user/driver/id/<int:pk>/rides/<int:n>/date/<str:date>/<int:is_after>
    def test_getDriverRideHistory(self):
        resp = self.client.get(reverse('getDriverRideHistory', kwargs={'pk': 1, 'n': 2, 'date':"2000-01-01", 'is_after':1}))
        self.assertContains(resp, 'DC')

    # User 3 is not a driver, so the ride list is empty
    def test_getDriverRideHistory_empty(self):
        resp = self.client.get(reverse('getDriverRideHistory', kwargs={'pk': 3, 'n': 2, 'date':"2000-01-01", 'is_after':1}))
        self.assertContains(resp, 'error')

    
