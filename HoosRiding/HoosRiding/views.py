from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

#used to prevent an csrf error (security)
from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
import json

from Hoos_Riding_API.models import User

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
