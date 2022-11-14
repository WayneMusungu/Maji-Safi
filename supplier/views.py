from django.shortcuts import render, get_object_or_404, redirect  
from .forms import SupplierForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Supplier
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_supplier

# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def supplierProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    supplier = get_object_or_404(Supplier, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        supplier_form = SupplierForm(request.POST, request.FILES, instance=supplier)
        
        if profile_form.is_valid() and supplier_form.is_valid():
            profile_form.save()
            supplier_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('supplierProfile')
        
        else:
            print(profile_form.errors)
            print(supplier_form.errors)
            
    else:
        profile_form = UserProfileForm(instance = profile)
        supplier_form = SupplierForm(instance = supplier)
    
    context = {
        'profile_form':profile_form,
        'supplier_form':supplier_form,
        'profile':profile,
        'supplier':supplier,
    }
    return render(request, 'supplier/supplierProfile.html', context)

def services(request):
    return render(request, 'supplier/services.html')
