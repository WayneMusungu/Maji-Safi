from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SupplierForm, OpeningHourForm
from accounts.forms import UserProfileForm
from services.forms import WaterProductForm, WaterTypeForm
from django.db import IntegrityError


from accounts.models import UserProfile, User
from .models import Supplier, OpeningHour
from services.models import Type, Product

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_supplier
from django.template.defaultfilters import slugify
from orders.models import Order, OrderedProduct

# Create your views here.

class SupplierProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        supplier = get_object_or_404(Supplier, user=request.user)
        profile_form = UserProfileForm(instance=profile)
        supplier_form = SupplierForm(instance=supplier)
        
        context = {
            'profile_form': profile_form,
            'supplier_form': supplier_form,
            'profile': profile,
            'supplier': supplier,
        }
        return render(request, 'supplier/supplierProfile.html', context)
    
    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        supplier = get_object_or_404(Supplier, user=request.user)
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
        
        context = {
            'profile_form': profile_form,
            'supplier_form': supplier_form,
            'profile': profile,
            'supplier': supplier,
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


def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(supplier=get_supplier(request))
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'supplier/opening_hours.html', context)


def add_opening_hours(request):
    """
    Handle data and save them inside the database
    """
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            # print(day,from_hour,to_hour,is_closed )
            try:
                hour = OpeningHour.objects.create(supplier=get_supplier(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                day = OpeningHour.objects.get(id=hour.id)
                if day.is_closed:
                    response = {'status': 'success', 'id':hour.id, 'day': day.get_day_display(), 'is_closed':'Closed'}
                else:
                    response = {'status': 'success', 'id':hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour':hour.to_hour}
                return JsonResponse (response)
            except IntegrityError as e:
                response = {'status': 'failed', 'message':from_hour+'-'+to_hour+' already exists for this day!'}
                return JsonResponse(response)

        else:
            HttpResponse('Invalid request')


def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id': pk})


def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_product = OrderedProduct.objects.filter(order=order, productitem__supplier=get_supplier(request))
        # print(ordered_product)
        # print(order)
        context = {
            'order':order,
            'ordered_product':ordered_product,
            'subtotal': order.get_total_by_supplier()['subtotal'],
            'tax_data':order.get_total_by_supplier()['tax_dict'],
            'grand_total':order.get_total_by_supplier()['grand_total'],
        }
    except:
        return redirect('supplier')
    return render(request, 'supplier/order_detail.html', context)


class MyOrdersView(ListView):
    model = Order
    template_name = 'supplier/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        supplier = Supplier.objects.get(user=self.request.user)
        return Order.objects.filter(suppliers__in=[supplier.id], is_ordered=True).order_by('-created_at')