import urllib.request
import urllib.parse
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

#helper method

# Home Page
def createDriverURL(driver_id, number_of_rides, date, is_after):
    return 'http://models-api:8000/api/user/driver/id/'+str(driver_id)+ '/rides/'+str(number_of_rides) + '/date/'+str(date)+"/"+str(is_after)

def createPassengerURL(rider_id, number_of_rides, date, is_after):
    return 'http://models-api:8000/api/user/id/'+str(rider_id)+ '/rides/'+str(number_of_rides) + '/date/'+str(date)+"/"+str(is_after)

def createFetchAvailableRides(number_of_rides, date, is_after):
    return 'http://models-api:8000/api/rides/n/'+str(number_of_rides)+'/date/'+str(date)+'/'+str(is_after)

# Detail Methods
def getRide(id):
    return getJsonFromRequest('http://models-api:8000/api/rides/'+str(id))
def getVehicle(id):
    return getJsonFromRequest('http://models-api:8000/api/vehicles/'+str(id))

def getUser(id):
    return getJsonFromRequest('http://models-api:8000/api/users/'+str(id))


def getJsonFromRequest(url):
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

def getHomePage(request):
    # Prob have a set of variables

    # Calling the Ride offered by the driver
  
    driver_current_rides = getJsonFromRequest(createDriverURL(1, 5, '2020-02-20-20', 1))
    driver_past_rides = getJsonFromRequest(createDriverURL(1, 5, '2020-02-20-20', 0))

    passenger_current_rides = getJsonFromRequest(createPassengerURL(1, 5, '2020-02-20-20', 1))
    passenger_past_rides = getJsonFromRequest(createPassengerURL(1, 5, '2020-02-20-20', 0))

    most_recent_ride_availible = getJsonFromRequest(createFetchAvailableRides(5, '2020-02-20-20',1))
 
    return JsonResponse({
        "driver_current_rides":driver_current_rides,
        "driver_previous_rides":driver_past_rides,
        "rides_getting_current_rides": passenger_current_rides,
        "rides_getting_past": passenger_past_rides,
        "most_recent_rides_available": most_recent_ride_availible
        })
        

def getDetailPage(request, pk):

    ride_json = getRide(pk)
    passengers = ride_json['passengers']
    vehicle_json = getVehicle(ride_json['vehicle'])
    driver_json = getUser(vehicle_json['driver'])
    
    passengers_json = {"seats_offered": ride_json['seats_offered']}

    #cleaning up needless data
    del vehicle_json['driver']
    del ride_json['passengers']
    del ride_json['seats_offered']
    del ride_json['vehicle']


    for passenger in passengers:
        passengers_json[str(passenger)] = getUser(passenger)
    
    #get vehicle info // lP, model, color
    #get driver info // FN, LN, P#, Profile URL
    #get passenger info // FN, LN, P#, Profile URL

    return JsonResponse({
        "ride": ride_json,
        "driver": driver_json,
        "passengers":passengers_json,
        "vehicle": vehicle_json
    })