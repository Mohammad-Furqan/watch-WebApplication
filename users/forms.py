from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import UserDetail

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    phone_number = PhoneNumberField()
    address = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','address' ,'phone_number', 'password1', 'password2']

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['address']