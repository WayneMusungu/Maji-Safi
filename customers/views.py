from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.views import View
from django.views.generic import ListView
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.mixins import CustomerRoleRequiredMixin
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import Order, OrderedProduct
import simplejson as json
from django.core.cache import cache

from django.contrib.auth.mixins import LoginRequiredMixin

class CustomerProfileView(LoginRequiredMixin, CustomerRoleRequiredMixin, View):
   login_url = 'login' 

   def get(self, request):
      profile = get_object_or_404(UserProfile, user=request.user)
      profile_form = UserProfileForm(instance=profile)
      user_form = UserInfoForm(instance=request.user)
      context = {
         'profile_form': profile_form,
         'user_form': user_form,
         'profile': profile,
      }
      return render(request, 'customers/customerProfile.html', context)

   def post(self, request):
      profile = get_object_or_404(UserProfile, user=request.user)
      profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
      user_form = UserInfoForm(request.POST, instance=request.user)

      if profile_form.is_valid() and user_form.is_valid():
         with transaction.atomic():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('customerProfile')
      else:
         print(profile_form.errors)
         print(user_form.errors)
         context = {
               'profile_form': profile_form,
               'user_form': user_form,
               'profile': profile,
         }
         return render(request, 'customers/customerProfile.html', context)
   
   
class MyOrdersView(LoginRequiredMixin, CustomerRoleRequiredMixin, ListView):
   login_url = 'login'
   template_name = 'customers/my_orders.html'
   context_object_name = 'orders'
   
   def get_queryset(self):
      user = self.request.user
      cache_key =  f'my_orders_{user.username}_{user.id}'
      orders = cache.get(cache_key)
      
      if orders:
         print("Retrieving from cache")
         print(f"Cache key: {cache_key}") 
         print(f"Cached orders: {orders}")
         
      else:
         print("Retrieving from database")
         orders = Order.objects.filter(user=user, is_ordered=True).order_by('-created_at')
         cache.set(cache_key, orders, timeout=300) # Cache timeout of 5 minutes
         
      return orders

class OrderDetailView(LoginRequiredMixin, CustomerRoleRequiredMixin, View):
    login_url = 'login'

    def get(self, request, order_number):
        cache_key = f'order_detail_{order_number}'
        context = cache.get(cache_key)

        if context:
            print("Retrieving from cache")
        else:
            print("Retrieving from database")
            try:
                order = Order.objects.get(order_number=order_number, is_ordered=True)
                ordered_product = OrderedProduct.objects.filter(order=order)
                
                # Calculate subtotal
                subtotal = sum(item.price * item.quantity for item in ordered_product)
                tax_data = json.loads(order.tax_data)
                
                context = {
                    'order': order,
                    'ordered_product': ordered_product,
                    'subtotal': subtotal,
                    'tax_data': tax_data,    
                }
                cache.set(cache_key, context, timeout=300)  # Cache timeout of 5 minutes
            except Order.DoesNotExist:
                return redirect('customer')
        
        return render(request, 'customers/order_detail.html', context)
         