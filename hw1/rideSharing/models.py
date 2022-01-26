from ast import mod
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse

TYPE_CHOICES = (
    ("SUV", "SUV"),
    ("COMPACT", "COMPACT"),
    ("SEDAN", "SEDAN"),
    ("COUPE", "COUPE"),
    ("OTHER", "OTHER"),
    ("--", "--")
)

class VehicleType(models.TextChoices):
    SUV = 'SU', _('SUV')
    COMPACT = 'CT', _('Compact')
    SEDAN = 'CD', _('Cedan')
    COUPE = 'CP', _('Coupe')
    OTHER = 'OT', _('Other')

class RideStatus(models.TextChoices):
    OPEN = 'O', _('Open')
    COMFIRMED = 'F', _('Comfirmed')
    COMPLETE = 'C', _('Complete')


class Vehicle(models.Model):
    #vehicle-owner
    vehicle_owner = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    
    # vehicle info
    vehicle_type = models.CharField(max_length=2,choices=VehicleType.choices)
    plate_num = models.CharField(max_length=8)
    seats = models.PositiveIntegerField(default=1)
    special_info = models.TextField(max_length=400,blank=True)

    def __str__(self):
        return self.vehicle_type + "Driver: " + self.vehicle_owner.username

    def get_absolute_url(self):
        return reverse('driverPage')


class Ride(models.Model):
    # onwer data
    owner = models.ForeignKey(User, on_delete=models.CASCADE)   # the owner of this ride  
    addr = models.CharField(max_length=100)    # destination
    arrive_date = models.DateTimeField(help_text='Format: 2022-01-01 12:00')
    required_type = models.CharField(max_length=2,choices=VehicleType.choices)
    passenger_num = models.PositiveIntegerField(default=1)
    special_requirements = models.CharField(max_length=400, blank=True)
    allow_share = models.BooleanField(default=False)
    
    # driver data(根据user_name检索)
    driver = models.CharField(default='', max_length=50, blank=True, null=True)

    #sharer data(根据user_name检索)
    sharer = models.CharField(default='', max_length=50, blank=True, null=True)
    sharer_seats = models.PositiveIntegerField(default=0)

    # order status
    status = models.CharField(max_length=1,choices=RideStatus.choices,default=RideStatus.OPEN)

    def __str__(self):
        return "owner:"+ self.owner.username + " addr: "+ self.addr

    # When submit, the webpage will go to the certain place
    def get_absolute_url(self):
        return reverse('rideSharing-home')


'''
IDEA:
所有客户用的都是自带的user数据结构。判断当前user是不是司机，可以去数据库中搜索有没有对应当前user的车。有，则是司机。
ride中owner,driver,sharer都是user类型的。
'''