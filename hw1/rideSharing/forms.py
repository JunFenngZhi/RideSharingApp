from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import VehicleType


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateRideForm(forms.Form):
    VEHICLE_TYPE_CHOICES = [
        ("SU", "Sedan"),
        ("CT", "Compact"),
        ("SD", "SUV"),
        ("CP", "Coupe"),
        ("OT", "Other")
    ]
    addr = forms.CharField(max_length=100)    # destination
    arrive_date = forms.DateTimeField(help_text='Format: 2022-01-01 12:00')
    required_type = forms.CharField(
        max_length=2, widget=forms.widgets.Select(choices=VEHICLE_TYPE_CHOICES))
    passenger_num = forms.IntegerField(initial=1)
    special_requirements = forms.CharField(max_length=400, required=False)
    allow_share = forms.BooleanField(initial=False, required=False)


class RequestSharingForm(forms.Form):
    addr = forms.CharField(label='Your Destination', max_length=100)
    earlist_time = forms.DateTimeField(label='Earlist Time of Arrival',input_formats='2022-01-01 12:00')
    latest_time = forms.DateTimeField(label='Latest Time of Arrival',input_formats='2022-01-01 12:00')
    special_requirements = forms.CharField(max_length=400, required=False)
    #num_sharer= forms.IntegerField(label='Number of Passengers in your Party')
