from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from datetime import datetime, timedelta
from django.core import serializers

# Used to generate authenticator
import os
import hmac
from .settings import SECRET_KEY

import json
from .models import User, Vehicle, Ride,Authenticator

from django.contrib.auth import hashers 
#Helper method
#Convert rides queryset into dict & filters by depart time

#The param """""""is_after""""""""""""
# if it's 1, it means it's after this date
# date = 2020/20/02/10 & is_after = True then,
# It's gonna fetch all rides after 2020/20/02/10

def convertTime(date):
    date = date[11:]
    am_or_pm = 'am'
    time = int(date)
    if(time>12):
        time = time - 12
        am_or_pm = 'pm'
    return str(time)+am_or_pm

def convertToDate(date):
    day = date[8:11]
    month = date[5:7]
    year = date[:4]
    return str(day+month+'/'+year)

def convertRidesToDict(rides,driver_id = -1):
    rides_as_dict = []
    for ride in rides:
        passengers_ids = [user.id for user in model_to_dict(ride)['passengers']]
        seats_filled = len(passengers_ids)
        seats_left = ride.seats_offered - seats_filled
        
        rides_as_dict.append({
            'special_time_fmt': ride.depart_time,
            'ride_id': ride.id,
            'vehicle': ride.vehicle.id,
            'passengers': passengers_ids,
            'destination': ride.destination,
            'start': ride.start,
           'hr': convertTime(ride.depart_time),
            'date': convertToDate(ride.depart_time),
            'seats_offered':ride.seats_offered,
            'price':ride.price,
            'seats_left': seats_left,
            'seats_filled': seats_filled,
            'driver_id': driver_id,
        }) 

    return {"rides":rides_as_dict}

#returns true if time is greater or equal
# Format is YYYY-MM-DD as strings
def compareTime(old_time, new_time):
    old_time = old_time.split("-")
    new_time = new_time.split("-")

    for i in range(3):
        prev = int(old_time[i])
        new = int(new_time[i])

        if(prev > new):
            return False

        elif(prev < new):
            return True

        else:
            pass

    return True


def isAuthTokenValid(request, auth_str):
    if(request.method == "GET"):
        pass
    else:
        return JsonResponse({"error": "Not a get"})
    current_time = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().replace(year= datetime.now().year+2).strftime("%Y-%m-%d")
    try:
        obj = Authenticator.objects.get(authenticator = auth_str)
        if(compareTime(obj.date_created, current_time)):
            return JsonResponse({"error": "Expired Token"})
        else:
            return JsonResponse({"valid": "Correct Token"})
    except Authenticator.DoesNotExist:
        return JsonResponse({"error": "Auth token does not exist!!"})

#Query Methods
@csrf_exempt
def createAuthenticator(request, user_id):
    user_model_instance = 0
    if(request.method == "POST"):
        pass
        #Checks if user exist in DB
        try:
            user_model_instance = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "No user exist with id:"+str(user_id)})

        #Creates authenticator
        authenticator_str = hmac.new(
            key = SECRET_KEY.encode('utf-8'),
            msg = os.urandom(32),
            digestmod = 'sha256',
        ).hexdigest()
  
        # Does authenticator exist?
        try:

            obj = Authenticator.objects.get(authenticator = authenticator_str)
            
            return createAuthenticator(request, user_id)
        except Authenticator.DoesNotExist:
            
            #Gets current and future time in case of update
            current_time = datetime.now().strftime("%Y-%m-%d")
            future_time = datetime.now().replace(year= datetime.now().year+1).strftime("%Y-%m-%d")
            #Below line test date conditional
            #current_time = future_time
            
            #Updates authenticator or creates new one for user
            try:
                authenticator = Authenticator.objects.get(user_id = user_id)
                if(compareTime(authenticator.date_created, current_time)):
                    authenticator.date_created = future_time
                    authenticator.authenticator = authenticator_str
                    authenticator.save()
                 
                #return JsonResponse({"error": "No reason to call. Authenticator valid!"})
                return JsonResponse(model_to_dict(authenticator))

            except Authenticator.DoesNotExist:
                authenticator = Authenticator(
                user = user_model_instance,
                authenticator = authenticator_str,
                date_created = future_time,
                )
                authenticator.save()
                return JsonResponse(model_to_dict(authenticator))

    return JsonResponse({"error": "Not a post method!"})


# returns ride history or current rides given
def getDriverRideHistory(request, pk, n, date, is_after):
    date = date.replace('-', '/')
    vehicles = Vehicle.objects.filter(driver = pk)
    rides_for_all_vehicles = []

    for vehicle in vehicles:
        if(is_after == 1):
            rides = Ride.objects.filter(vehicle = vehicle.id, depart_time__gt = date).order_by('depart_time')[:n]
            rides_for_all_vehicles.extend(convertRidesToDict(rides)['rides'])
        elif(is_after == 0):
            rides = Ride.objects.filter(vehicle = vehicle.id, depart_time__lte = date).order_by('depart_time')[:n]
            rides_for_all_vehicles.extend(convertRidesToDict(rides)['rides'])
        else:
            return JsonResponse({"error": "improper is_after url param! Can only be 1 or 0"})
    
    sorted_rides = sorted(rides_for_all_vehicles, key=lambda k: k['special_time_fmt'])

    return JsonResponse({"rides":sorted_rides})
   # return sorted(total_rides, key=lambda k: k['date']) 


    return JsonResponse(rides_for_all_vehicles)

def getNUserRideHistory(request, pk, n, date, is_after):
    date = date.replace('-', '/')
    if(is_after == 1):
        rides = Ride.objects.filter(passengers=pk, depart_time__gt = date).order_by('depart_time')[:n]
        return JsonResponse(convertRidesToDict(rides,pk))
    elif(is_after == 0):
        rides = Ride.objects.filter(passengers=pk, depart_time__lte = date).order_by('depart_time')[:n]
        return JsonResponse(convertRidesToDict(rides,pk))
    else:
        return JsonResponse({"error": "Incorrect 'is_after' param! Should be 1 or 0 "})

# Home page thing, get rides from the soonest
def getNSoonestRides(request, n, date, is_after):
    date = date.replace('-', '/')

    #Gets all rides sorted where I get N rides that are oldest
    if(is_after == 1):
        rides = Ride.objects.filter(depart_time__gt = date).order_by('depart_time')[:n]
        rides_arr = convertRidesToDict(rides)["rides"]
        
        return JsonResponse(convertRidesToDict(rides))
    elif(is_after == 0):
        rides = Ride.objects.filter(depart_time__lte = date).order_by('depart_time')[:n]
        return JsonResponse(convertRidesToDict(rides))
    else:
        return JsonResponse({"error": "Incorrect 'is_after' param! Should be 1 or 0 "})

@csrf_exempt
def user(request, pk=-1):
# pk:int - this is user id
    if request.method == 'GET':
        user = User.objects.get(pk=pk)
        return JsonResponse(model_to_dict(user))

# first_name:str
# last_name:str
# phone_number:str
# profile_url:url
    elif request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        try:
            user_model_instance = User.objects.get(username = json_data["username"])
            return JsonResponse({"error": "Username Exist already"})
        except User.DoesNotExist:
            pass

        user = User(
            first_name=json_data["first_name"],
            last_name=json_data["last_name"],
            phone_number=json_data["phone_number"],
            profile_url=json_data["profile_url"],
            username = json_data["username"],
            password = hashers.make_password(json_data["password"]),
            )
        user.save()

        return JsonResponse(model_to_dict(user))

# first_name:str
# last_name:str
# phone_number:str
# profile_url:url
# user_id:int
    elif request.method == 'PUT':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        User.objects.filter(pk=pk).update(first_name=json_data["first_name"], last_name=json_data["last_name"],
                    phone_number=json_data["phone_number"], profile_url=json_data["profile_url"])
        return JsonResponse(json_data)

# pk:int - this is user id
    elif request.method == 'DELETE':
        user = User.objects.get(pk=pk)
        user.delete()
        return JsonResponse({"key": "value"})
        

@csrf_exempt
def vehicle(request, pk=-1):

# vehicle_id:int
    if request.method == 'GET':
        vehicle = Vehicle.objects.get(pk=pk)
        return JsonResponse(model_to_dict(vehicle))
# first_name:str
# last_name:str
# phone_number:str
# profile_url:url
# user_id:int
    elif request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        user = User.objects.get(pk=json_data['driver'])
        vehicle = Vehicle(
            driver=user,
            license_plate=json_data['license_plate'],
            model=json_data['model'],
            color=json_data['color'], #capacity=json_data['capacity']
        )
        vehicle.save()
        return JsonResponse(json_data)

# first_name:str
# last_name:str
# phone_number:str
# profile_url:url
# user_id:int
    elif request.method == 'PUT':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        user = User.objects.get(pk=json_data['driver'])
        Vehicle.objects.filter(pk=pk).update(driver=user,license_plate=json_data['license_plate'],
                          model=json_data['model'], color=json_data['color'])
        return JsonResponse(json_data)

# pk - vehicle id 
    elif request.method == 'DELETE':
        vehicle = Vehicle.objects.get(pk=pk)
        vehicle.delete()
        return JsonResponse({"key": "value"})
    else:
        return HttpResponse(status=400)                

def getAllVehicles(request):
    data = serializers.serialize("json", Vehicle.objects.all())
    struct = json.loads(data)
    return HttpResponse(struct)

@csrf_exempt
def ride(request, pk=-1, uid = -1):

# pk - ride id
    if request.method == 'GET':
        if(uid != -1):
            return JsonResponse({"error": "improper url"})

        ride = Ride.objects.get(pk=pk)
        vehicle = ride.vehicle
        passengers = User.objects.filter(ride=pk)
        return JsonResponse({
            'vehicle': vehicle.id,
            'passengers': [model_to_dict(x)['id'] for x in passengers],
            'destination': ride.destination,
            'start': ride.start,
            'depart_time': ride.depart_time,
            'seats_offered':ride.seats_offered,
            'price':ride.price
        })
    
# vehicle:int vehicle id
# destination:str
# start:str
# depart_time: str
# seats_offered: int
# price: int
    elif request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        vehicle = Vehicle.objects.get(pk=json_data['vehicle'])

        ride = Ride(
            vehicle = vehicle,
            destination = json_data['destination'],
            start = json_data['start'],
            depart_time = json_data['depart_time'],
            price = json_data['price'],
            seats_offered = json_data['seats_offered']
            )
        ride.save()

        return JsonResponse(json_data)
    elif request.method == 'PUT':
        if(uid != -1):
            ride = Ride.objects.get(pk=pk)
            prospective_rider = User.objects.get(pk=uid)
            passengers = User.objects.filter(ride=pk)
            
            if(ride.vehicle.driver.id == prospective_rider.id):
                return JsonResponse({"key":"error"})
            else:
                ride.passengers.add(prospective_rider)
            return JsonResponse({"key": "success"})

# driver:int - user id (making request to create)
    
# first_name:str
# last_name:str
# phone_number:str
# profile_url:url
# user_id:int
    elif request.method == 'DELETE':
        ride = Ride.objects.get(pk=pk) 
        ride.delete()
        return JsonResponse({"key": "value"})
    else:
        return HttpResponse(status=400)
    return HttpResponse(status = 400)
