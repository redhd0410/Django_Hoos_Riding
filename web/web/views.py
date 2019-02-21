import urllib.request
import urllib.parse
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

def getJsonFromRequest(url):
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

def homepage(request):
    ride_information = getJsonFromRequest("http://exp-api:8000/experience/homepage/get")
    return render(request,'homepage.html', ride_information)

def ridedetails(request):
     ride_information = getJsonFromRequest("http://exp-api:8000/experience/detailpage/get/1")
    return render(request,'ridedetails.html', ride_information)