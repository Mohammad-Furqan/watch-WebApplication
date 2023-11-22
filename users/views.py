from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User

# Create your views here.
from .models import UserDetail

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
            else:
                user = form.save()
                phone_number = form.cleaned_data.get('phone_number')
                address = form.cleaned_data.get('address')
                UserDetail.objects.create(user=user, phone_number=phone_number, address=address)
                messages.success(request, f'{username}! Your account has been created! You can login now.')
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})











# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             # Check if the username already exists
#             username = form.cleaned_data.get('username')
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username already exists. Please choose a different username.')
#             else:
#                 form.save()
#                 messages.success(request, f'{username}! Your account has been created! You can login now.')
#                 return redirect('login')
#     else:
#         form = UserRegisterForm()      
#     return render(request, 'users/register.html', {'form': form})