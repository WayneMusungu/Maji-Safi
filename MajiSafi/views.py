from django.shortcuts import render
from django.http import HttpResponse
from supplier.models import Supplier


def home(request):
    """
    Show approved and active Suppliers on the homepage
    """
    suppliers = Supplier.objects.filter(is_approved=True, user__is_active=True)[:10]
    print(suppliers)
    context = {
        "suppliers":suppliers,
    }
    return render(request, "home.html", context)