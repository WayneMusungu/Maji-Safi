from django.shortcuts import render, get_object_or_404, redirect  
from .forms import SupplierForm
from accounts.forms import UserProfileForm
from services.forms import WaterProductForm, WaterTypeForm

from accounts.models import UserProfile
from .models import Supplier
from services.models import Type, Product

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_supplier
from django.template.defaultfilters import slugify

# Create your views here.

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


@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def services(request):
    """
    Get the logged in Supplier and get multiple queryset of the type of services they offer
    """
    supplier = Supplier.objects.get(user=request.user)
    types = Type.objects.filter(supplier=supplier)
    context = {
        'types': types,
    }
    return render(request, 'supplier/services.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def water_by_type(request, pk=None):
    supplier = Supplier.objects.get(user=request.user)
    type = get_object_or_404(Type, pk=pk)
    products = Product.objects.filter(supplier=supplier, type=type)
    context = {
        'products': products,
        'type': type,
    }
    print(products)
    return render(request, 'supplier/water_by_type.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def add_type(request): 
    if request.method == 'POST':
        form = WaterTypeForm(request.POST)
        if form.is_valid():
            """
            Assign the supplier before storing the form
            """
            water_type_name = form.cleaned_data['water_type']
            water = form.save(commit=False)
            water.supplier = Supplier.objects.get(user=request.user)
            water.save() # The water id will be generated
            """
            Generate a slug based on the water type name
            """
            water.slug = slugify(water_type_name)+'-'+str(water.id) # mineral-water-15
            water.save()
            
            messages.success(request, f'{water_type_name} has been added to your dashboard')
            return redirect('services')
        else:
            print(form.errors)
    else:
        form = WaterTypeForm()
    context = {
        'form': form,   
    }
    return render(request, 'supplier/add_type.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def edit_type(request, pk=None):
    water_type_name = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        form = WaterTypeForm(request.POST, instance=water_type_name)
        if form.is_valid():
            """
            Assign the supplier before storing the form
            """
            water_type_name = form.cleaned_data['water_type']
            water = form.save(commit=False)
            water.supplier = Supplier.objects.get(user=request.user)
            """
            Generate a slug based on the water type name
            """
            water.slug = slugify(water_type_name)+'-'+str(water.id) 
            form.save()
            
            messages.success(request, f'{water_type_name} has been updated successfully')
            return redirect('services')
        else:
            print(form.errors)
    else:
        form = WaterTypeForm(instance=water_type_name)
    context = {
        'form': form, 
        'water_type_name' : water_type_name 
    }
    return render(request, 'supplier/edit_type.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_supplier)  
def delete_type(request, pk=None):
    water_type_name = get_object_or_404(Type, pk=pk)
    water_type_name.delete()
    messages.success(request,f'{water_type_name} has been removed from your dashboard')
    return redirect(services)

def get_supplier(request):
            supplier = Supplier.objects.get(user=request.user)
            return supplier
        
        
@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def add_product(request):
    if request.method == 'POST':
        form = WaterProductForm(request.POST, request.FILES)
        if form.is_valid():
            """
            Assign the supplier before storing the form
            """
            bottle_size = form.cleaned_data['bottle_size']
            bttle_water = form.save(commit=False)
            bttle_water.supplier = Supplier.objects.get(user=request.user)
            bttle_water.slug = slugify(bottle_size) 
            form.save()
            
            messages.success(request, f'{bottle_size} Water Product has been added successfully')
            return redirect('water_by_type', bttle_water.type.id)
        else:
            print(form.errors)
    else:
        form = WaterProductForm()
        """
        Create a function to modify the form fields to show only the type of water that belongs to a specific logged in Supplier
        """
        # def get_supplier(request):
        #     supplier = Supplier.objects.get(user=request.user)
        #     return supplier
        
        form.fields['type'].queryset = Type.objects.filter(supplier = get_supplier(request))
          
    context ={
        'form':form,
    }
    return render (request, 'supplier/add_product.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def edit_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = WaterProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            bottlesize = form.cleaned_data['bottle_size']
            product = form.save(commit=False)
            product.supplier = Supplier.objects.get(user=request.user)
            product.slug = slugify(bottlesize) 
            form.save()
            
            messages.success(request, f'{bottlesize} has been updated successfully')
            return redirect('water_by_type', product.type.id)
        else:
            print(form.errors)
    else:
        form = WaterProductForm(instance=product)
        form.fields['type'].queryset = Type.objects.filter(supplier = get_supplier(request))

    context = {
        'form': form, 
        'product' : product,
    }
    return render(request, 'supplier/edit_product.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_supplier)
def delete_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, f'{product} has been removed from your dashboard')
    return redirect('water_by_type', product.type.id)

    
    
