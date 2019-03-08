import urllib.request
import urllib.parse
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import logging
from web.forms import *

#Logger definition
# logger = logging.getLogger(__name__)

def getJsonFromRequest(url):
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

# Only takes dictionaries as bodies 
def postJsonFromRequest(url, body):
    data = json.dumps(body)
    data = str(data)   
    post_encoded = data.encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded)    
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)
    
@csrf_exempt
def createaccount(request):
    if request.method == 'POST':
        caform = createaccountForm(request.POST)
        if caform.is_valid():
            data = caform.cleaned_data
            resp = postJsonFromRequest("http://exp-api:8000/experience/createaccount", data)
             
             #Sets cookie
            response = redirect('http://localhost:8000')
            response.set_cookie('first_cookie',resp["authenticator"])
            return response
    else: 
        caform = createaccountForm()
    return render(request, 'createaccount.html', {'caform': caform})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        loginform = loginForm(request.POST)
        if loginform.is_valid():
            data = loginform.cleaned_data
             #Sets cookie
            return render(request, 'login.html', {'loginform': loginform})
    else: 
        loginform = loginForm()
    return render(request, 'login.html', {'loginform': loginform})

@csrf_exempt
def homepage(request):
    auth_cookie = request.COOKIES.get('first_cookie')
    if(auth_cookie):
        ride_information = getJsonFromRequest("http://exp-api:8000/experience/homepage/get/"+str(auth_cookie))
        if("error" in ride_information):
            return redirect("http://localhost:8000/createaccount") 
        else:
            return render(request,'homepage.html', ride_information)
    else:
        return redirect("http://localhost:8000/createaccount")

def ridedetails(request, pk):
    ride_information = getJsonFromRequest("http://exp-api:8000/experience/detailpage/get/"+str(pk)+"/"+ auth_cookie)
    return render(request,'ridedetails.html', ride_information)

#def createListing(request):
#    form = createListingForm()
#    return render(request, 'createListing.html', {'form': form})