import urllib.request
import urllib.parse
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict


#helper method
def createDriverURL(driver_id, number_of_rides, date, is_after):
    return 'http://models-api:8000/api/user/driver/id/'+str(driver_id)+ '/rides/'+str(number_of_rides) + '/date/'+str(date)+"/"+str(is_after)

def getHomePage(request):
    # Prob have a set of variables

    # Calling the Ride offered by the driver
    req = urllib.request.Request(createDriverURL(1, 5, '2020-02-20-20', 1))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    driver_current_rides = json.loads(resp_json)

    req = urllib.request.Request(createDriverURL(1, 5, '2020-02-20-20', 0))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    driver_past_rides = json.loads(resp_json)    

    return JsonResponse({
        "driver_current_rides":driver_current_rides,
        "driver_previous_rides":driver_past_rides
        })

def getDetailPage():
    print("s")