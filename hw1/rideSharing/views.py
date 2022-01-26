from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import context
from django.views.generic.edit import CreateView
#from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm
from .models import Ride,Vehicle


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
    # 创建表单，获取发起request的用户的信息，将form封装成dict传入render
    u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form
    }
    return render(request, 'rideSharing/home.html', context=context)


# Show orders
@login_required
def showAllOrders(request):
    return render(request, 'rideSharing/showAllorders.html')

# request a sharing order. User becomes rider sharer
@login_required
def requestSharing(request):
    return render(request, 'rideSharing/requestSharing.html')


# driverPage. User registers a vehicle or accepts an order
class driverPage(CreateView):
    model = Vehicle
    fields = ['vehicle_type', 'plate_num','special_info','seats']
    template_name = 'rideSharing/driverPage.html'

    def form_valid(self, form):
        form.instance.vehicle_owner = self.request.user   # 将当前操作写入owner字段
        return super().form_valid(form)



# request an order. User becomes ride owner
class requestOrder(CreateView):
    model = Ride
    fields = ['addr', 'arrive_date', 'passenger_num','required_type','special_requirements','allow_share']
    template_name = 'rideSharing/requestOrder.html'
    # success_url = '/home'  # 使用这个参数需要在前面加一个/回到上一层，不用这个参数则使用model.get_absolute_url()函数替代

    def form_valid(self, form):
        form.instance.owner = self.request.user   # 将当前操作写入owner字段
        return super().form_valid(form)