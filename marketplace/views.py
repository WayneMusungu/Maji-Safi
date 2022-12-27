from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from supplier.models import OpeningHour, Supplier
from services.models import Type, Product
from .models import Cart
from django.db.models import Prefetch
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime

# Create your views here.

def marketplace(request):
    suppliers = Supplier.objects.filter(is_approved=True, user__is_active=True)
    supplier_count = suppliers.count()
    context = {
        "suppliers":suppliers,
        "supplier_count":supplier_count,
    }
    return render(request, 'marketplace/listings.html', context)


def supplier_detail(request, supplier_slug):
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
    # print(today)
    # print(today_date)
    current_opening_hours = OpeningHour.objects.filter(supplier=supplier, day=today)
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # print(current_time)
    # print(now)
    """
    Check if there is multiple opening hours in the same day and determine whether the water shop is opened/closed during a specific time frame
    """
    is_open = None
    for current in current_opening_hours:
        start = str(datetime.strptime(current.from_hour, "%I:%M %p").time())
        end = str(datetime.strptime(current.to_hour, "%I:%M %p").time())
        print(start, end)
        if current_time > start and current_time < end:
            is_open = True
            break
        else:
            is_open = False
        # print(is_open)
    
    # print(current_opening_hours)
    
    
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
        "is_open": is_open,
    }
    return render(request, 'marketplace/supplier_detail.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
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
                    return JsonResponse({'status': 'Success', 'message': 'Increased the Cart Quantity', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    checkCart = Cart.objects.create(user=request.user, product=product, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'This Product has been added to your Cart!', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})     

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This Product does not exist!'})     
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})       
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
     
    
def decrease_cart(request, product_id):
    if request.user.is_authenticated:
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
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your Cart!'})     

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This Product does not exist!'})     
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})       
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
   

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        "cart_items": cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


@login_required(login_url='login')
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the Cart Item Exist
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart Item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)}) 
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})  
                
                    
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})   
        
        
def search(request):
    address = request.GET['address']
    keyword = request.GET['keyword']
    # print(address, keyword)
   
    """
    Get Supplier ids that has the water type that a user is looking for
    """
    fetch_supplier_by_product = Product.objects.filter(bottle_size__icontains=keyword, is_available=True).values_list('supplier', flat=True)# Get the list of Supplier ids 
    # print(fetch_supplier_by_product)
    
    fetch_supplier_by_water_type = Type.objects.filter(water_type__icontains=keyword).values_list('supplier', flat=True)
    # print(fetch_supplier_by_water_type)
    
    suppliers = Supplier.objects.filter(Q(id__in=fetch_supplier_by_product) | Q(id__in=fetch_supplier_by_water_type) | Q(supplier_name__icontains=keyword, is_approved=True, user__is_active=True))
    
    # suppliers = Supplier.objects.filter(supplier_name__icontains=keyword, is_approved=True, user__is_active=True)
        # print(suppliers)
    supplier_count = suppliers.count()
    
    context = {
        'suppliers': suppliers,
        'supplier_count': supplier_count,
    }
    return render(request, 'marketplace/listings.html', context)
            
   

    
        
