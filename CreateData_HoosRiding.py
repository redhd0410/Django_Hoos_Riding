import urllib.request
import urllib.parse
import json
from datetime import datetime
from datetime import timedelta

#Likely to not work
def getJsonFromRequest(url):
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

def postJsonFromRequest(url, data):
    data = json.dumps(data)
    data = str(data)   
    post_encoded = data.encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded)    
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')


models_layer = "http://localhost:8001/api/"
#print(getJsonFromRequest("http://localhost:8001/api/users/1"))


def createUsers(users):
    for id,user in enumerate(users):
        user_json = {
        "username": user,
        "password": user,
        "first_name": user,
        "last_name":user,
        "phone_number": "1112223333",
        "profile_url": "http://www.google.com"
        }
        postJsonFromRequest(models_layer+"users/0", user_json)
        postJsonFromRequest(models_layer+ "authenticator/"+str(id+1),{"na":"na"})

def createVehicles(vehicles):
    for vehicle in vehicles:

        vehicle_json = {
            "driver": vehicle,
            "license_plate": vehicle,
            "model":"CAR",
            "color":"BLACK"
        }
        postJsonFromRequest(models_layer+"vehicles/0",vehicle_json)


def createRides(rides):
    for raw_ride in rides:
        ride = raw_ride.split("|")
        ride_json= {
            "vehicle":ride[0],
            "destination":ride[2],
            "start":ride[1],
            "depart_time":"2008/11/14/01",
            "seats_offered":int(ride[4]),
            "price":int(ride[5])
        }
        postJsonFromRequest(models_layer+"rides/0", ride_json)


users = ["A", "B", "C","D",
        "E", "F", "G"]

vehicles = ["1", "5"]

#Only two vehicle id's: 1, 5
rides = [
    "1|B|C|after|3|10",
    "1|A|C|after|4|15"
    ]

#Creates sets of users
createUsers(users)
createVehicles(vehicles)
createRides(rides)

#print(datetime.today().strftime('%Y-%m-%d-%H'))

#print((datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d-%H'))