from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

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