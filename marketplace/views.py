from django.shortcuts import render, get_object_or_404
from supplier.models import Supplier

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
    context = {
        "supplier":supplier,
    }
    return render(request, 'marketplace/supplier_detail.html', context)
