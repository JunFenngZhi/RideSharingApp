from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import context
from django.views.generic.edit import CreateView
#from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UpdateRideForm, UserRegisterForm, UserUpdateForm, RequestSharingForm
from .models import Ride, RideStatus, Vehicle


# create the register page. usingn register.html template.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'You account have already created. You can login now!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'rideSharing/register.html', {'form': form})


# create home page after login
@login_required
def home(request):
    is_driver = Vehicle.objects.filter(
        vehicle_owner_id=request.user.id).exists()
    # 创建表单，获取发起request的用户的信息，将form封装成dict传入render
    u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
        'is_driver': is_driver,
    }
    return render(request, 'rideSharing/home.html', context=context)

############################################################
# myOrders related pages

@login_required
def showAllOrders(request):
    return render(request, 'rideSharing/showAllorders.html')


@login_required
def showOwnerOrders(request):
    # get all the open orders requested by current user
    openRide_list = Ride.objects.filter(
        status=RideStatus.OPEN, owner=request.user)
    openRide_list = openRide_list.order_by('arrive_date')

    # get all the conformed orders requested by current user
    conformed_list = Ride.objects.filter(
        status=RideStatus.CONFIRMED, owner=request.user)
    conformed_list = conformed_list.order_by('arrive_date')

    # get all the complete orders requested by current user
    completedRide_list = Ride.objects.filter(
        status=RideStatus.COMPLETE, owner=request.user)
    completedRide_list = completedRide_list.order_by('arrive_date')

    context = {
        'openRide_list': openRide_list,
        'conformed_list': conformed_list,
        'completedRide_list': completedRide_list
    }

    return render(request, 'rideSharing/showOwnerOrders.html', context=context)


@login_required
def editOwnerOrders(request, id):
    if request.method == "POST":
        ride_form = UpdateRideForm(request.POST)
        if ride_form.is_valid():  # 获取数据
            addr = ride_form.cleaned_data['addr']
            arrive_date = ride_form.cleaned_data['arrive_date']
            required_type = ride_form.cleaned_data['required_type']
            passenger_num = ride_form.cleaned_data['passenger_num']
            special_requirements = ride_form.cleaned_data['special_requirements']
            # create the ride
            cur_ride = Ride.objects.get(id=id)
            cur_ride.addr = addr
            cur_ride.arrive_date = arrive_date
            cur_ride.required_type = required_type
            cur_ride.passenger_num = passenger_num
            cur_ride.special_requirements = special_requirements
            cur_ride.save()
            return redirect('showOwnerOrders')  # 自动跳转回上一层

    ride_form = UpdateRideForm()
    return render(request, 'rideSharing/editOwnerOrders.html', locals())


@login_required
def deleteOwnerOrders(request, id):
    Ride.objects.get(id=id).delete()
    return redirect('showOwnerOrders')  # 自动跳转回上一层


@login_required
def showVehicle(request, id):
    # 通过当前订单的司机名字定位到对应的user,用外键反查到该司机对应的车辆。
    cur_ride = Ride.objects.get(id=id)
    driver_name = cur_ride.driver
    driver = User.objects.filter(username=driver_name).first()
    shownVehicle = driver.owner_vehicle

    context = {
        'shownVehicle': shownVehicle
    }

    return render(request, 'rideSharing/showVehicle.html', context)


@login_required
def showDriverOrders(request):
    # get all the conformed orders requested by current user
    conformed_list = Ride.objects.filter(
        status=RideStatus.CONFIRMED, driver=request.user.username)
    conformed_list = conformed_list.order_by('arrive_date')

    # get all the complete orders requested by current user
    completedRide_list = Ride.objects.filter(
        status=RideStatus.COMPLETE, driver=request.user.username)
    completedRide_list = completedRide_list.order_by('arrive_date')

    context = {
        'conformed_list': conformed_list,
        'completedRide_list': completedRide_list
    }

    return render(request, 'rideSharing/showDriverOrders.html', context=context)


@login_required
def completeDriverOrders(request, id):
    ride = Ride.objects.filter(pk=id).first()
    ride.status = RideStatus.COMPLETE
    ride.save()

    return redirect('showDriverOrders')

@login_required
def showSharerOrders(request):
    # get all the open orders requested by current user
    openRide_list = Ride.objects.filter(
        status=RideStatus.OPEN, sharer=request.user)
    openRide_list = openRide_list.order_by('arrive_date')

    # get all the conformed orders requested by current user
    conformed_list = Ride.objects.filter(
        status=RideStatus.CONFIRMED, sharer=request.user)
    conformed_list = conformed_list.order_by('arrive_date')

    # get all the complete orders requested by current user
    completedRide_list = Ride.objects.filter(
        status=RideStatus.COMPLETE, sharer=request.user)
    completedRide_list = completedRide_list.order_by('arrive_date')

    context = {
        'openRide_list': openRide_list,
        'conformed_list': conformed_list,
        'completedRide_list': completedRide_list
    }

    return render(request, 'rideSharing/showOwnerOrders.html', context=context)


############################################################
# Sharer related pages
# request a sharing order. User becomes rider sharer
@login_required
def requestSharing(request):
    if request.method == 'POST':
        joinid = request.POST.get('ride_to_join')
        if joinid is not None:
            ride_to_join = Ride.objects.get(id=joinid)
            ride_to_join.sharer = request.user.username
            ride_to_join.sharer_seats = request.POST.get('n_seats')
            ride_to_join.totalRequiredSeats = ride_to_join.totalRequiredSeats + int(request.POST.get('n_seats'))
            ride_to_join.save()
        joinid = request.POST.get('ride_to_cancel')
        if joinid is not None:
            ride_to_join = Ride.objects.get(id=joinid)
            ride_to_join.sharer = ""
            ride_to_join.totalRequiredSeats = ride_to_join.totalRequiredSeats - ride_to_join.sharer_seats
            ride_to_join.sharer_seats = 0
            ride_to_join.save()

    form = RequestSharingForm(request.GET)
    if form.is_valid():
        show_result = True
        addr = form.cleaned_data.get('addr')
        earlist_time = form.cleaned_data.get('earlist_time')
        latest_time = form.cleaned_data.get('latest_time')
        special_requirements = form.cleaned_data.get('special_requirements')
        #num_sharer = form.cleaned_data.get('num_sharer')
        canidate_list = Ride.objects.filter(
            status=RideStatus.OPEN,
            allow_share=True,
            addr__exact=addr,
            arrive_date__lte=latest_time,
            arrive_date__gte=earlist_time,
            sharer="",
            # driver__seats__gte=F('passenger_num')+num_sharer,
        )
        if special_requirements:
            ride_list = canidate_list.filter(special_requirements=special_requirements)
        else:
            ride_list = canidate_list
        # if special_requirements:
        #     ride_list = []
        #     for ride in canidate_list:
        #         car = Vehicle.objects.get(vehicle_owner__username=ride.driver)
        #         if car.special_info == special_requirements:
        #             ride_list.append(ride)
        # else:
        #     ride_list = canidate_list
    else:
        show_result = False
        ride_list = Ride.objects.filter(status=RideStatus.OPEN)
    
    joined_list = Ride.objects.filter(
        status=RideStatus.OPEN,
        allow_share=True,
        sharer=request.user.username,
    )

    context = {
        'form': form,
        'ride_list': ride_list,
        'joined_list': joined_list,
        'show_result': show_result,
    }
    return render(request, 'rideSharing/requestSharing.html', context=context)


############################################################
# Driver related pages
# driverPage. User registers a vehicle or accepts an order
class driverVehicleRegister(CreateView):
    model = Vehicle
    fields = ['vehicle_type', 'plate_num', 'special_info', 'seats']
    template_name = 'rideSharing/driverVehicleRegister.html'

    def form_valid(self, form):
        form.instance.vehicle_owner = self.request.user   # 将当前操作写入owner字段
        return super().form_valid(form)


# driver search for order
def driverSearchOrder(request):
    # 只显示乘客人数匹配载客量且车辆类型符合要求的订单
    car_info = Vehicle.objects.filter(
        vehicle_owner=request.user).first()  # 获取当前用户拥有的车辆(假如返回空，怎么处理/)
    ride_list = Ride.objects.filter(status=RideStatus.OPEN,
                                    required_type=car_info.vehicle_type,
                                    totalRequiredSeats__lte=car_info.seats)
    ride_list = ride_list.exclude(owner=request.user)
    ride_list = ride_list.order_by('arrive_date')
    context = {
        'object_list': ride_list,
    }

    return render(request, 'rideSharing/driverSearchOrder.html', context=context)


# driver Confirm Order
def driverConfirmOrder(request, rid):
    ride = Ride.objects.filter(pk=rid).first()
    ride.driver = request.user.username
    ride.status = RideStatus.CONFIRMED
    ride.save()
    return redirect('rideSharing-home')


############################################################
# Owner related pages
# request an order. User becomes ride owner
class ownerRequestOrder(CreateView):
    model = Ride
    fields = ['addr', 'arrive_date', 'passenger_num',
              'required_type', 'special_requirements', 'allow_share']
    template_name = 'rideSharing/ownerRequestOrder.html'
    # success_url = '/home'  # 使用这个参数需要在前面加一个/回到上一层，不用这个参数则使用model.get_absolute_url()函数替代

    def form_valid(self, form):
        form.instance.owner = self.request.user   # 将当前操作写入owner字段
        form.instance.totalRequiredSeats = form.instance.passenger_num  # not test
        return super().form_valid(form)
