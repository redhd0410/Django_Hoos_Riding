import urllib.request
import urllib.parse
import json
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import logging
from web.forms import *


def getJsonFromRequest(url):
    #Force fixing issue
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

# Only takes dictionaries as bodies 
#
# MUST HAVE FOWARD LAST AS LAST CHARACTER!!!!!! FOR URL
#
@csrf_exempt
def postJsonFromRequest(url, body):

    #Does not convert from bytes
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
            resp = postJsonFromRequest("http://exp-api:8000/experience/login/", data)
            
            if("error" in resp):
                return redirect("http://localhost:8000/login")

            response = redirect('http://localhost:8000')
            response.set_cookie('first_cookie',resp["authenticator"])
            return response
    else: 
        loginform = loginForm()
    return render(request, 'login.html', {'loginform': loginform})

def LogOut(request):
    auth_cookie = request.COOKIES.get('first_cookie')
    response = redirect("http://localhost:8000")
    if auth_cookie:
        response.delete_cookie('first_cookie')
    return response

def createListing(request):
    auth_cookie = request.COOKIES.get('first_cookie')
    if not auth_cookie: 
        return redirect(reverse("login") + "?next=" + reverse("createlisting"))

    if request.method == 'POST':

        form = createListingForm(request.POST)
        if (form.is_valid()):
            data = form.cleaned_data
            resp = postJsonFromRequest("http://exp-api:8000/experience/createlisting/"+str(auth_cookie), data)
            response = redirect('http://localhost:8000')
            return response

    form = createListingForm()
    return render(request, 'createlisting.html', {'form': form})    

@csrf_exempt
def homepage(request):
    auth_cookie = request.COOKIES.get('first_cookie')
    if(auth_cookie):
        ride_information = getJsonFromRequest("http://exp-api:8000/experience/homepage/get/"+str(auth_cookie))
        if("error" in ride_information):
            return HttpResponse(ride_information['error'])
            return redirect("http://localhost:8000/createaccount") 
        else:
            return render(request,'homepage.html', ride_information)
    else:
        return redirect("http://localhost:8000/createaccount")

def ridedetails(request, pk):
    auth_cookie = request.COOKIES.get('first_cookie')
    if(auth_cookie):
        ride_information = getJsonFromRequest("http://exp-api:8000/experience/detailpage/get/"+str(pk)+"/"+ auth_cookie)
        return render(request,'ridedetails.html', ride_information)
    else:
        return redirect("http://localhost:8000")

@csrf_exempt
def search(request):
    if request.method == 'POST':
        searchform = searchForm(request.POST)
        if (searchform.is_valid()):
            data = searchform.cleaned_data
            try: 
                search_result = getJsonFromRequest("http://exp-api:8000/experience/search/"+str(data['search_keyword']))
                context = {'searchform' : searchform, 'result': search_result}
                return render(request, 'searchresult.html', context)
            except:
                context = {'searchform' : searchform, 'result': "Data does not exist."}
                return render(request, 'searchresult.html', context)
    else: 
        searchform = searchForm()
    return render(request, 'searchresult.html', {'searchform' : searchform})