from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from supplier.models import OpeningHour, Supplier
from services.models import Type, Product
from .models import Cart
from django.db.models import Prefetch
from .context_processors import get_cart_counter, get_cart_amounts
from django.db.models import Q
from datetime import date
from orders.forms import OrderForm
from accounts.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class MarketPlaceView(View):
    def get(self, request):
        suppliers = Supplier.objects.filter(is_approved=True, user__is_active=True)
        supplier_count = suppliers.count()
        context = {
            "suppliers":suppliers,
            "supplier_count":supplier_count,
        }
        return render(request, 'marketplace/listings.html', context)
    
    
class SupplierDetailView(View):
    def get(self, request, supplier_slug):
    
        supplier = get_object_or_404(Supplier, supplier_slug=supplier_slug)
        """
        Type class model we have no access to Product class model therefore we use Prefetch to reverse look up Product class model
        """
        water_type = Type.objects.filter(supplier=supplier).prefetch_related(
            Prefetch(
                "products",
                queryset = Product.objects.filter(is_available=True),
            )
        )
        
        opening_hours = OpeningHour.objects.filter(supplier=supplier).order_by('day','from_hour')
        
        """
        Check current day's opening hours
        """
        today_date = date.today()
        today = today_date.isoweekday()
        
        current_opening_hours = OpeningHour.objects.filter(supplier=supplier, day=today)
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
        else:
            cart_items=None
        context = {
            "supplier":supplier,
            "water_type":water_type,
            "cart_items":cart_items,
            "opening_hours":opening_hours,
            "current_opening_hours": current_opening_hours,
            
        }
        return render(request, 'marketplace/supplier_detail.html', context)


class AddCartView(LoginRequiredMixin, View):    
    def handle_no_permission(self):
        return JsonResponse({'status': 'login_required', 'message':'Please login to continue'})
    
    def get(self, request, product_id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the Product exist
            try:
                product = Product.objects.get(id=product_id)
                """
                Check if the user has already added Product to the cart, and increase the cart quantity otherwise create a new cart for the Product
                
                """
                try:
                    checkCart = Cart.objects.get(user=request.user, product=product)
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Increased the Cart Quantity', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': checkCart.quantity, 
                        'cart_amount': get_cart_amounts(request)
                    })
                except:
                    checkCart = Cart.objects.create(user=request.user, product=product, quantity=1)
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'This Product has been added to your Cart!', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': checkCart.quantity, 
                        'cart_amount': get_cart_amounts(request)
                    })     

            except:
                return JsonResponse({
                    'status': 'Failed', 
                    'message': 'This Product does not exist!'
                })     
        else:
            return JsonResponse({
                'status': 'Failed', 
                'message': 'Invalid Request!'
            })       
    
                    
class DecreaseCartView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

    def get(self, request, product_id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the Product exist
            try:
                product = Product.objects.get(id=product_id)
                """
                Check if the user has already added Product to the cart, if the number of Products is greater than one,
                then we decrease the quantity and if it is less than one we simply delete the Product

                """
                try:
                    checkCart = Cart.objects.get(user=request.user, product=product)
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({
                        'status': 'Success', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': checkCart.quantity, 
                        'cart_amount': get_cart_amounts(request)
                    })
                except Cart.DoesNotExist:
                    return JsonResponse({
                        'status': 'Failed', 
                        'message': 'You do not have this item in your Cart!'
                    })

            except Product.DoesNotExist:
                return JsonResponse({
                    'status': 'Failed', 
                    'message': 'This Product does not exist!'
                })
        else:
            return JsonResponse({
                'status': 'Failed', 
                'message': 'Invalid Request!'
            })    


class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'marketplace/cart.html'
    context_object_name = 'cart_items'
    login_url = 'login'
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).order_by('created_at')


class DeleteCartView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request, cart_id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                print(f"Attempting to delete cart item with id: {cart_id}")
                # Check if the Cart Item Exist
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                cart_item.delete()
                print(f"Deleted cart item with id: {cart_id}")
                return JsonResponse({
                    'status': 'Success', 
                    'message': 'Cart Item has been deleted!', 
                    'cart_counter': get_cart_counter(request), 
                    'cart_amount': get_cart_amounts(request)
                }) 
            except Cart.DoesNotExist:
                print(f"Cart item with id {cart_id} does not exist")
                return JsonResponse({
                    'status': 'Failed', 
                    'message': 'Cart Item does not exist!'
                })  
        else:
            print("Invalid request type")
            return JsonResponse({
                'status': 'Failed', 
                'message': 'Invalid Request!'
            })
        
class SearchView(View):
      
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '') 
        print(query)
    
        """
        Get Supplier ids that has the water type or bottle size that a user is looking for
        """
        fetch_supplier_by_product = Product.objects.filter(bottle_size__icontains=query, is_available=True).values_list('supplier', flat=True)
        
        fetch_supplier_by_water_type = Type.objects.filter(water_type__icontains=query).values_list('supplier', flat=True)
        
        suppliers = Supplier.objects.filter(
            Q(id__in=fetch_supplier_by_product) | 
            Q(id__in=fetch_supplier_by_water_type) | 
            Q(supplier_name__icontains=query) &
            Q(is_approved=True, user__is_active=True)
        )
        
        supplier_count = suppliers.count()
        
        context = {
            'suppliers': suppliers,
            'supplier_count': supplier_count,
        }
        return render(request, 'marketplace/listings.html', context)
   
        
class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
        cart_count = cart_items.count()
        
        # If cart count is 0, redirect user to the marketplace page
        if cart_count <= 0:
            return redirect('marketplace')
        
        # Assign the value of logged in user to prepopulate the OrderForm
        user_profile = UserProfile.objects.get(user=request.user)
        default_values = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'county': user_profile.county,
            'town': user_profile.town,
            'pin_code': user_profile.pin_code,     
        }
        form = OrderForm(initial=default_values)
        context = {
            'form': form,
            'cart_items': cart_items,
        }
        return render(request, 'marketplace/checkout.html', context)
        
