from django.http import HttpResponse
from django.shortcuts import render, redirect
from supplier.forms import SupplierForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth


# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect ('myAccount')
    elif request.method == 'POST':
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


def registerSupplier(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect ('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        supplier_form = SupplierForm(request.POST, request.FILES)
        if form.is_valid() and supplier_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.WATER_SUPPLIER
            user.save()
            supplier = supplier_form.save(commit = False)
            supplier.user = user
            """
            Get the user profile fom the UserProfile Model.
            When the user.save is trigerred, 
            Signals will create the user profile of the user
            """
            user_profile = UserProfile.objects.get(user=user)
            supplier.user_profile = user_profile
            supplier.save()
            messages.success(request, "Your account has been registered successfully!! Kindly wait for approval from the admin")
            return redirect('registerSupplier')

        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        supplier_form = SupplierForm()
    context ={
        'form':form,
        'supplier_form': supplier_form,
    }
    return render(request, 'accounts/registerSupplier.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        """
        Use Django inbuilt authenticate function
        """
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You have logged out")
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')