from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# used to prevent an csrf error (security)
from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
import json
import datetime
from Hoos_Riding_API.models import User, Vehicle, Ride

def home(request):
    return render(request, "index.html", {})

@csrf_exempt
def user(request, pk=-1):

# pk:int - this is user id 
    if request.method == 'GET':
        user = User.objects.get(pk=pk)
        return JsonResponse(model_to_dict(user))

# first_name:str,
# last_name:str,
# phone_number:str,
# profile_url:url
    elif request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        user = User(
            first_name=json_data["first_name"],
            last_name=json_data["last_name"],
            phone_number=json_data["phone_number"],
            profile_url=json_data["profile_url"]
            )
        user.save()
        return JsonResponse(json_data)

# first_name:str,
# last_name:str,
# phone_number:str,
# profile_url:url,
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
# first_name:str,
# last_name:str,
# phone_number:str,
# profile_url:url,
# user_id:int
    elif request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        user = User.objects.get(pk=json_data['driver'])
        vehicle = Vehicle(
            driver=user,
            license_plate=json_data['license_plate'],
            model=json_data['model'],
            color=json_data['color'], capacity=json_data['capacity']
        )
        vehicle.save()
        return JsonResponse(json_data)

# first_name:str,
# last_name:str,
# phone_number:str,
# profile_url:url,
# user_id:int
    elif request.method == 'PUT':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        user = User.objects.get(pk=json_data['driver'])
        Vehicle.objects.filter(pk=pk).update(driver=user,license_plate=json_data['license_plate'],
                          model=json_data['model'], color=json_data['color'], capacity=json_data['capacity'])
        return JsonResponse(json_data)

# pk - vehicle id 
    elif request.method == 'DELETE':
        vehicle = Vehicle.objects.get(pk=pk)
        vehicle.delete()
        return JsonResponse({"key": "value"})
    else:
        return HttpResponse(status=400)                

@csrf_exempt
def ride(request, pk=-1, uid = -1):

# pk - ride id
    if request.method == 'GET':
        ride = Ride.objects.get(pk=pk)
        vehicle = ride.vehicle
        passengers = User.objects.filter(ride=pk)
        return JsonResponse({
            'vehicle': model_to_dict(vehicle),
            'passengers': [model_to_dict(x)['id'] for x in passengers],
            'destination': ride.destination,
            'start': ride.start,
            'depart_time': ride.depart_time,
            'seats_offered':ride.seats_offered,
            'price':ride.price
        })
    
# vehicle:int vehicle id,  destination:str, start:str, depart_time: str, seats_offered: int, price: int
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

        return JsonResponse({"key":"val"})
    elif request.method == 'PUT':
        if(uid != -1):
            ride = Ride.objects.get(pk=pk)
            passenger = User.objects.get(pk=uid)
            if(ride.vehicle.driver.id == passenger.id):
                return JsonResponse({"key":"error"})
            else:
                ride.passengers.add(passenger)
            return JsonResponse({"key": "success"})

# driver:int - user id (making request to create)
        
# first_name:str, last_name:str, phone_number:str, profile_url:url, user_id:int
    elif request.method == 'DELETE':
        ride = Ride.objects.get(pk=pk) 
        ride.delete()
        return JsonResponse({"key": "value"})
    else:
        return HttpResponse(status=400)
    return HttpResponse(status = 400)
