from django.urls import path    
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required




urlpatterns = [
    # system entrance and exit
    path('', auth_views.LoginView.as_view(template_name='rideSharing/login.html'), name='login'),  # enter login page first
    path('logout/', auth_views.LogoutView.as_view(template_name='rideSharing/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # home page menu
    path('home/', views.home, name='rideSharing-home'),

    # all orders
    path('showAllOrders/', views.showAllOrders, name='showAllOrders'),
    path('showOwnerOrders/', views.showOwnerOrders, name='showOwnerOrders'),
    path('editOwnerOrders/<int:id>', views.editOwnerOrders, name='editOwnerOrders'),
    #path('showVehicle/<int:id>', views.showVehicle, name='showVehicle'),
    
    # driver
    path('driverVehicleRegister/', login_required(views.driverVehicleRegister.as_view()), name='driverVehicleRegister'),
    path('driverSearchOrder/', views.driverSearchOrder, name='driverSearchOrder'),
    path('driverConfirmOrder/<int:rid>', views.driverConfirmOrder, name='driverConfirmOrder'),

    # owner
    path('ownerRequestOrder/', login_required(views.ownerRequestOrder.as_view()), name='ownerRequestOrder'),

    # sharer
    path('requestSharing/', views.requestSharing, name='requestSharing')
]