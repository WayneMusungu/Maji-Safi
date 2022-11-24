from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from supplier.models import Supplier
from services.models import Type, Product
from .models import Cart
from django.db.models import Prefetch

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
    Type class model we have no access to Product class model therefore we use Pref etch to reverse look up Product class model
    """
    water_type = Type.objects.filter(supplier=supplier).prefetch_related(
        Prefetch(
            "products",
            queryset = Product.objects.filter(is_available=True),
        )
    )
    context = {
        "supplier":supplier,
        "water_type":water_type,
    }
    return render(request, 'marketplace/supplier_detail.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the Product exist
            try:
                product = Product.objects.get(id=product_id)
                """
                Check if the user has already addded food to the cart, and increase the cart quantity otherwise create a new cart for the Product
                
                """
                try:
                    checkCart = Cart.objects.get(user=request.user, product=product)
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the Cart Quantity'})
                except:
                    checkCart = Cart.objects.create(user=request.user, product=product, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'This Product has been added to your Cart!'})     

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This Product does not exist!'})     
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})       
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    """
    Use httpresponse to avoid reloading the page
    """
    # return HttpResponse(product_id)
    
