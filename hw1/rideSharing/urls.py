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
    path('requestOrder/', login_required(views.requestOrder.as_view()), name='requestOrder'),
    path('showAllOrders/', views.showAllOrders, name='showAllOrders'),
    path('driverPage/', login_required(views.driverPage.as_view()), name='driverPage'),
    path('requestSharing/', views.requestSharing, name='requestSharing')



]