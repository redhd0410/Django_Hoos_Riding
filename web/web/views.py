import urllib.request
import urllib.parse
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

def homepage(request):
    ride_information = {
    "rides_getting_past": {},
    "driver_current_rides": {
        "1": {
            "1": {
                "depart_time": "2020/02/30/06",
                "start": "Cville",
                "price": 10,
                "vehicle": 1,
                "passengers": [
                    2,
                    3
                ],
                "seats_offered": 3,
                "ride_id": 1,
                "destination": "Arlington"
            },
            "2": {
                "depart_time": "2020/03/20/06",
                "start": "Arlington",
                "price": 10,
                "vehicle": 1,
                "passengers": [
                    2,
                    3,
                    4
                ],
                "seats_offered": 3,
                "ride_id": 2,
                "destination": "Cville"
            }
        }
    },
    "most_recent_rides_available": {
        "4": {
            "depart_time": "2018/12/25/16",
            "start": "Alexandria",
            "price": 15,
            "vehicle": 1,
            "passengers": [
                3
            ],
            "seats_offered": 1,
            "ride_id": 4,
            "destination": "Arlington"
        },
        "5": {
            "depart_time": "2017/12/25/16",
            "start": "Alexandria",
            "price": 15,
            "vehicle": 1,
            "passengers": [],
            "seats_offered": 1,
            "ride_id": 5,
            "destination": "Arlington"
        }
    },
    "driver_previous_rides": {
        "1": {
            "4": {
                "depart_time": "2018/12/25/16",
                "start": "Alexandria",
                "price": 15,
                "vehicle": 1,
                "passengers": [
                    3
                ],
                "seats_offered": 1,
                "ride_id": 4,
                "destination": "Arlington"
            },
            "5": {
                "depart_time": "2017/12/25/16",
                "start": "Alexandria",
                "price": 15,
                "vehicle": 1,
                "passengers": [],
                "seats_offered": 1,
                "ride_id": 5,
                "destination": "Arlington"
            }
        }
    },
    "rides_getting_current_rides": {}
    }
    return render(request,'homepage.html', ride_information)

def ridedetails(request):
    return render(request,'ridedetails.html')