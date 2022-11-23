from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from supplier.models import Supplier
from services.models import Type, Product
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
    """
    Use httpresponse to avoid reloading the page
    """
    return HttpResponse(product_id)
    
