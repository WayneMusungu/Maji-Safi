from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import Order
# Create your views here.

@login_required(login_url='login')
def customerProfile(request):
    # Show the existing values inside the form field of a logged in customer
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
      profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
      user_form = UserInfoForm(request.POST, instance=request.user)
      
      if profile_form.is_valid() and user_form.is_valid():
         profile_form.save()
         user_form.save()
         messages.success(request, 'Profile updated')
         return redirect('customerProfile')
      else:
         print(profile_form.errors)
         print(user_form.errors)
    
    else:
      profile_form = UserProfileForm(instance=profile)
      user_form = UserInfoForm(instance=request.user)
    
    context = {
       'profile_form': profile_form,
       'user_form': user_form ,
       'profile': profile,
    }
    return render(request, 'customers/customerProfile.html', context)
 

@login_required(login_url='login') 
def my_orders(request):
   orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at') # Show the recent order
   context = {
      'orders': orders,
   }
   return render( request, 'customers/my_orders.html', context)
