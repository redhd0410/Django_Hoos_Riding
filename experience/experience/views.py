import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

#helper methods for easier api requests
        
# Home Page
def createDriverURL(driver_id, number_of_rides, date, is_after):
    return 'http://models-api:8000/api/user/driver/id/'+str(driver_id)+ '/rides/'+str(number_of_rides) + '/date/'+str(date)+"/"+str(is_after)

def createPassengerURL(rider_id, number_of_rides, date, is_after):
    return 'http://models-api:8000/api/user/id/'+str(rider_id)+ '/rides/'+str(number_of_rides) + '/date/'+str(date)+"/"+str(is_after)

def createFetchAvailableRides(number_of_rides, date, is_after):
    return 'http://models-api:8000/api/rides/n/'+str(number_of_rides)+'/date/'+str(date)+'/'+str(is_after)

# Detail Methods
#Get methods
def getRide(id):
    return getJsonFromRequest('http://models-api:8000/api/rides/'+str(id))
def getVehicle(id):
    return getJsonFromRequest('http://models-api:8000/api/vehicles/'+str(id))

def getUser(id):
    return getJsonFromRequest('http://models-api:8000/api/users/'+str(id))

def isGoodCookie(auth_str):
    resp = getJsonFromRequest("http://models-api:8000/api/checkcookie/"+str(auth_str))
    return resp
    

# Experience layer function calls for internal user

def getJsonFromRequest(url):
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

def postJsonFromRequest(url, body):
    data = json.loads(str(body,encoding = 'utf-8'))
    data = json.dumps(data)
    data = str(data)   
    post_encoded = data.encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded)    
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)


# Main Experience Layer(Called from Web Layer)
@csrf_exempt
def getHomePage(request, auth):
    cookie_response = isGoodCookie(auth)
    if("error" not in cookie_response):
        pass
    else:
        return HttpResponse(str(cookie_response))
    # Calling the Ride offered by the driver
    # Current Date
    date = '2019-03-10-20'
  
    driver_current_rides = getJsonFromRequest(createDriverURL(1, 5, date, 1))
    driver_past_rides = getJsonFromRequest(createDriverURL(1, 5, date, 0))

    passenger_current_rides = getJsonFromRequest(createPassengerURL(1, 5, date, 1))
    passenger_past_rides = getJsonFromRequest(createPassengerURL(1, 5, date, 0))

    most_recent_ride_availible = getJsonFromRequest(createFetchAvailableRides(5, date,1))
 
    return JsonResponse({
        "driver_current_rides":driver_current_rides,
        "driver_previous_rides":driver_past_rides,
        "rides_getting_current_rides": passenger_current_rides,
        "rides_getting_past": passenger_past_rides,
        "most_recent_rides_available": most_recent_ride_availible
        })


def getDetailPage(request,auth, pk):
    cookie_response = isGoodCookie(auth)
    if("error" not in cookie_response):
        pass
    else:
        return HttpResponse(str(cookie_response))
    ride_json = getRide(pk)
    passengers = ride_json['passengers']
    vehicle_json = getVehicle(ride_json['vehicle'])
    driver_json = getUser(vehicle_json['driver'])
    
#    seats_offered_json =ride_json['seats_offered']

    #cleaning up needless data
    del vehicle_json['driver']
    del ride_json['passengers']
    del ride_json['seats_offered']
    del ride_json['vehicle']

    passengers_json = {}

    for passenger in passengers:
        passengers_json[str(passenger)] = getUser(passenger)
        

    #get vehicle info // lP, model, color
    #get driver info // FN, LN, P#, Profile URL
    #get passenger info // FN, LN, P#, Profile URL

    return JsonResponse({
   #    "seats_offered": seats_offered_json,
        "ride": ride_json,
        "driver": driver_json,
        "passengers":passengers_json,
        "vehicle": vehicle_json
    })


#Post methods
@csrf_exempt
def createListing(request, auth):
    cookie_response = isGoodCookie(auth)
    if("error" not in cookie_response):
        pass
    else:
        return HttpResponse(str(cookie_response))

    data = json.loads(str(request.body,encoding = 'utf-8'))
    data["vehicle"] = getJsonFromRequest("http://models-api:8000/api/vehicles/"+str(auth))["vehicle_id"]
   
    data = json.dumps(data)
    data = str(data)
    post_encoded = data.encode('utf-8')
    req = urllib.request.Request("http://models-api:8000/api/rides", data=post_encoded)    
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')

    return JsonResponse(resp_json)

@csrf_exempt
def createAccount(request):
    resp = postJsonFromRequest("http://models-api:8000/api/users", request.body)    
    if('error' in resp):
        return JsonResponse(resp)
    auth_resp = postJsonFromRequest("http://models-api:8000/api/authenticator/"+str(resp['id']), request.body)
    if('error' in auth_resp):
        return JsonResponse(auth_resp)      
    return JsonResponse({'authenticator':auth_resp['authenticator']})
