from django.contrib import admin

from .models import Ride, Vehicle


class RideAdmin(admin.ModelAdmin):
    fields = ['addr', 'arrive_date', 'passenger_num', 'required_type',
              'special_requirements', 'allow_share', 'status', 'driver', 'sharer', 'sharer_seats', 'totalRequiredSeats']
    list_display = ('owner', 'addr', 'arrive_date','sharer','sharer_seats',
                    'passenger_num', 'required_type', 'status')
    list_filter = ['owner', 'status', 'totalRequiredSeats', 'sharer']


class VehicleAdmin(admin.ModelAdmin):
    fields = ['vehicle_owner', 'vehicle_type',
              'plate_num', 'seats', 'special_info']
    list_display = ('vehicle_owner', 'vehicle_type',
                    'plate_num', 'seats', 'special_info')
    list_filter = ['vehicle_owner']


admin.site.register(Ride, RideAdmin)
admin.site.register(Vehicle, VehicleAdmin)
