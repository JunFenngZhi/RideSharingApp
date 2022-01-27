from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

class RequestSharingForm(forms.Form):
    addr = forms.CharField(label='Your Destination', max_length=100)
    earlist_time = forms.DateTimeField(label='Earlist Time of Arrival',input_formats='2022-01-01 12:00')
    latest_time = forms.DateTimeField(label='Latest Time of Arrival',input_formats='2022-01-01 12:00')
    num_sharer= forms.IntegerField(label='Number of Passengers in your Party')