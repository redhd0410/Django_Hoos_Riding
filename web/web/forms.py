from django import forms

class createaccountForm(forms.Form):
    username = forms.CharField(max_length = 20, label="username")
    password = forms.CharField(max_length = 30, label="password", widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=30, label="first name")
    last_name = forms.CharField(max_length=30, label="last name")
    phone_number = forms.CharField(max_length=11, label="phone_number")
    profile_url = forms.URLField(label="profile_url")

class createListingForm(forms.Form):
    destination = forms.CharField(max_length=50)
    start = forms.CharField(max_length=50)
    depart_time = forms.CharField(max_length=13)
    seats_offered = forms.IntegerField()
    price = forms.IntegerField()

class loginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 30, widget=forms.PasswordInput())