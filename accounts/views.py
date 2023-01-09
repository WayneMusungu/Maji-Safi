from django.http import HttpResponse
from django.shortcuts import render, redirect
from supplier.forms import SupplierForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_email_verification
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from supplier.models import Supplier
from django.template.defaultfilters import slugify
from orders.models import Order



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
            
            # Send Email Verification to the Registered User
            """
            Create a helper function to send the verification email to the registered User
            """
            subject = 'Account Activation'
            email_template = 'accounts/emails/account_email_verification.html'
            send_email_verification(request, user, subject, email_template)
            
            messages.success(request, "Your account has been created, an activation link has been sent to your email")
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
            supplier_name = supplier_form.cleaned_data['supplier_name']
            supplier.supplier_slug = slugify(supplier_name) +'-'+str(user.id)
            """
            Get the user profile fom the UserProfile Model.
            When the user.save is trigerred, 
            Signals will create the user profile of the user
            """
            user_profile = UserProfile.objects.get(user=user)
            supplier.user_profile = user_profile
            supplier.save()
            
            # Send Email Verification to the Registered Supplier
            """
            Create a helper function to send the verification email to the registered Supplier
            """
            subject = 'Account Activation'
            email_template = 'accounts/emails/account_email_verification.html'

            send_email_verification(request, user, subject, email_template)
            
            messages.success(request, "Your account has been created, an activation link has been sent to your email. Kindly wait for approval from the admin")
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

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to true
    try:
        """Get the encoded uid and decode it."""
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated')
        return redirect('myAccount')
    else:  
        messages.error(request, 'Invalid activation link')  
        return redirect ('myAccount')    


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect ('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        """
        Use Django inbuilt authenticate function
        """
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You have logged out")
    return redirect('login')


"""
This function is responsible for detecting whether the User is a Customer or a Supplier and be taken to the respective dashboard
"""
@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


"""
Restricting customer from accessing the supplier's page
"""
def check_role_customer(user):
    if user.role == 2:
        return True
    else: 
        raise PermissionDenied
    
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:6]  # Show only six recent orders
    context = {
        'orders': orders,
        'orders_count': orders.count(),  # count the number of orders made by the customer
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/customerDashboard.html', context)


"""
Restricting Supplier from accessing the customers page
"""
def check_role_supplier(user):
    if user.role == 1:
        return True
    else: 
        raise PermissionDenied
    
@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def supplierDashboard(request):
    supplier = Supplier.objects.get(user=request.user)
    orders = Order.objects.filter(suppliers__in=[supplier.id], is_ordered=True).order_by('-created_at')
    # print(orders)
    # supplier = Supplier.objects.get(user=request.user)
    context = {
        'orders': orders,
        'orders_count': orders.count()
    }
    return render(request, 'accounts/supplierDashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            """
            Create a helper function for password reset email
            """
            
            # send_password_reset_email(request, user)
            subject = 'Password Reset'
            email_template = 'accounts/emails/reset_password_email.html'
            send_email_verification(request, user, subject, email_template)
            
            messages.success(request, 'Password reset link has been sent to your email address')
            return redirect('login')
            
        else:
            messages.error(request, 'An account with that email does not exist')
            return redirect('forgot_password')
            
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    """
    Validate the user by decoding the token and the user pk
    """
    try:
        """Get the encoded uid and decode it."""
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        """
        Store the uid inside the session because we need the pk to reset the password
        """
        request.session['uid'] = uid
        messages.info(request, 'Enter new password')
        return redirect('reset_password')
        
    else:
        messages.error(request, 'This link has expired')
        return redirect(myAccount)


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')