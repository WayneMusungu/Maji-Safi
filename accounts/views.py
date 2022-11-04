from django.http import HttpResponse
from django.shortcuts import render, redirect
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages

# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            """
            store password in a hashed format
            """
            # CREATE USER USING THE FORM
            
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            
            # CREATE USER USING THE CREATE USER METHOD
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully!!")
            print('The user has been created successfuly')            
            return redirect('registerUser')
        else:
            print('form is invalid')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render (request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.WATER_SUPPLIER
            user.save()
            vendor = vendor_form.save(commit = False)
            vendor.user = user
            """
            Get the user profile fom the UserProfile Model.
            When the user.save is trigerred, 
            Signals will create the user profile of the user
            """
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been registered successfully!! Kindly wait for approval from the admin")
            return redirect('registerVendor')

        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()
    context ={
        'form':form,
        'vendor_form': vendor_form,
    }
    return render(request, 'accounts/registerVendor.html', context)