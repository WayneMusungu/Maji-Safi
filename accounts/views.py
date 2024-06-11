import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from supplier.forms import SupplierForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from .utils import detectUser, send_email_verification
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from supplier.models import Supplier
from django.template.defaultfilters import slugify
from orders.models import Order
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db import transaction
from .mixins import CustomerRoleRequiredMixin


# Create your views here.
class RegisterUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('myAccount')
        form = UserForm()
        context = {'form': form}
        return render(request, 'accounts/registerUser.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('myAccount')
        
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    user.role = User.CUSTOMER
                    user.save()
                    
                    """
                    Create a helper function to send the verification email to the registered User
                    """
                    subject = 'Account Activation'
                    email_template = 'accounts/emails/account_email_verification.html'
                    send_email_verification(request, user, subject, email_template)
                    
                    messages.success(request, "Your account has been created, an activation link has been sent to your email")
                    print('The user has been created successfully')
                    return redirect('registerUser')
            except Exception as e:
                print('An error occurred during user registration:', e)
                messages.error(request, "An error occurred during user registration. Please try again later.")
                return redirect('registerUser')
        else:
            print('Form is invalid')
            print(form.errors)
            context = {'form': form}
            return render(request, 'accounts/registerUser.html', context)
            
        
class RegisterSupplierView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('myAccount')
        form = UserForm()
        supplier_form = SupplierForm()
        context ={
            'form': form,
            'supplier_form': supplier_form,
        }
        return render(request, 'accounts/registerSupplier.html', context)

    def post(self, request):
        form = UserForm(request.POST)
        supplier_form = SupplierForm(request.POST, request.FILES)
        if form.is_valid() and supplier_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                with transaction.atomic():
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    user.role = User.WATER_SUPPLIER
                    user.save()    
                    supplier = supplier_form.save(commit=False)
                    supplier.user = user
                    supplier_name = supplier_form.cleaned_data['supplier_name']
                    supplier.supplier_slug = slugify(supplier_name) + '-' + str(user.id)
                    
                    """
                    Get the user profile from the UserProfile Model.
                    When the user.save is triggered, 
                    Signals will create the user profile of the user
                    """
                    
                    user_profile = UserProfile.objects.get(user=user)
                    supplier.user_profile = user_profile
                    supplier.save()
                    
                    # Send Email Verification to the Registered Supplier
                    subject = 'Account Activation'
                    email_template = 'accounts/emails/account_email_verification.html'
                    send_email_verification(request, user, subject, email_template)
                    
                    messages.success(request, "Your account has been created, an activation link has been sent to your email. Kindly wait for approval from the admin")
                    return redirect('registerSupplier')

            except Exception as e:
                print('An error occurred during supplier registration:', e)
                messages.error(request, "An error occurred during supplier registration. Please try again later.")
                return redirect('registerSupplier')
        else:
            messages.error(request, "Invalid form")
            return render(request, 'accounts/registerSupplier.html', {'form': form, 'supplier_form': supplier_form})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated')
        else:  
            messages.error(request, 'Invalid activation link')
        
        return redirect('myAccount')  
    
    
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('myAccount')
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('myAccount')
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "You have logged out")
        return redirect('login')


class MyAccountView(View):
    """
    This function is responsible for detecting whether the User is a Customer or a Supplier and be taken to the respective dashboard
    """
    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request):
        user = request.user
        redirectUrl = detectUser(user)
        return redirect(redirectUrl)


class CustomerDashboardView(LoginRequiredMixin, CustomerRoleRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user, is_ordered=True)
        recent_orders = orders[:6]  # Show only six recent orders
        context = {
            'orders': orders,
            'orders_count': orders.count(),  # Count the number of orders made by the customer
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
    recent_orders = orders[:10]
    
    # Get The Current Month's Revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(suppliers__in=[supplier.id], created_at__month=current_month)
    # print(current_month_orders)
    
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_supplier()['grand_total']
    # print(current_month_revenue)
        
    # Total Revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_supplier()['grand_total']
    
    # print(orders)
    # supplier = Supplier.objects.get(user=request.user)
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue':total_revenue,
        'current_month_revenue':current_month_revenue,
    }
    return render(request, 'accounts/supplierDashboard.html', context)


class ForgotPassword(View):
    def get(self, request):
        return render(request, 'accounts/forgot_password.html')
    
    def post(self, request):
        email = request.POST.get('email')
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            """
            Create a helper function for password reset email
            """
            
            subject = 'Password Reset'
            email_template = 'accounts/emails/reset_password_email.html'
            send_email_verification(request, user, subject, email_template)
            
            messages.success(request, 'Password reset link has been sent to your email address')
            return redirect('login')
        
        else:
            messages.error(request, 'An account with that email does not exist')
            return redirect('forgot_password') 


class ResetPasswordValidateView(View):
    """
    Validate the user by decoding the token and the user pk
    """
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            """Get the encoded uid and decode it."""
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
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
            return redirect('myAccount')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'accounts/reset_password.html')
    
    def post(self, request):
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
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
