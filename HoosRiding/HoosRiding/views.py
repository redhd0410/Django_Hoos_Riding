from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

#used to prevent an csrf error (security)
from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
import json

from Hoos_Riding_API.models import User, Vehicle

def home(request):
    return render(request, "index.html", {})

@csrf_exempt
def user(request, pk=-1):
   if request.method == 'GET':
      if(pk == -1):
         return HttpResponse(status=400)
      user = User.objects.get(pk = pk)
      return JsonResponse(model_to_dict(user))

   elif request.method == 'POST':
      json_data = json.loads(str(request.body, encoding = 'utf-8'))
      user = User(first_name = json_data["first_name"], last_name = json_data["last_name"], phone_number = json_data["phone_number"], profile_url = json_data["profile_url"])
      user.save()
      return JsonResponse(json_data)

@csrf_exempt
def vehicle(request, pk = -1):
   if request.method == 'GET':
      if(pk == -1):
         return HttpResponse(status=400)
      vehicle = Vehicle.objects.get(pk = pk)
      return JsonResponse(model_to_dict(vehicle))

   elif request.method == 'POST':
      json_data = json.loads(str(request.body, encoding = 'utf-8'))
      user = User.objects.get(pk = json_data['driver'])
      vehicle = Vehicle(driver = user, license_plate = json_data['license_plate'], model = json_data['model'], color = json_data['color'], capacity = json_data['capacity'])
      vehicle.save()
      return JsonResponse(json_data)
