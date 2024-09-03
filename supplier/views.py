from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from accounts.mixins import SupplierRoleRequiredMixin
from supplier.utils import get_supplier
from .forms import SupplierForm, OpeningHourForm
from accounts.forms import UserProfileForm
from services.forms import WaterProductForm, WaterTypeForm
from django.db import IntegrityError
from accounts.models import UserProfile
from .models import Supplier, OpeningHour
from services.models import Type, Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_supplier
from django.template.defaultfilters import slugify
from orders.models import Order, OrderedProduct
from django.core.cache import cache

# Create your views here.

class SupplierProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
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
    
    def post(self, request):
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
    
    
class Services(LoginRequiredMixin, SupplierRoleRequiredMixin, ListView):
    login_url = 'login'
    
    model = Type
    template_name = "supplier/services.html"
    context_object_name = "types"
    
    def get_queryset(self):
        self.supplier = get_object_or_404(Supplier, user=self.request.user)
        return Type.objects.filter(supplier=self.supplier)
    

class WaterByTypeView(LoginRequiredMixin, SupplierRoleRequiredMixin, ListView):
    model = Product
    template_name = "supplier/water_by_type.html"
    context_object_name = "products"
    login_url = 'login'
    
    def get_queryset(self):
        self.supplier = get_object_or_404(Supplier, user=self.request.user)
        self.type = get_object_or_404(Type, pk=self.kwargs['pk'])
        return Product.objects.filter(supplier=self.supplier, type=self.type)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.type
        return context


class AddType(LoginRequiredMixin, SupplierRoleRequiredMixin, SuccessMessageMixin, CreateView):
    model = Type
    form_class = WaterTypeForm
    template_name = 'supplier/add_type.html'
    success_url = reverse_lazy('services')
    login_url = 'login'
    
    def form_valid(self, form):
        """
        Assign the supplier before saving the form
        """
        water_type_name = form.cleaned_data['water_type']
        water = form.save(commit=False)
        water.supplier = Supplier.objects.get(user=self.request.user)
        water.save()  # The water id will be generated
        
        """
        Generate a slug based on the water type name
        """
        water.slug = slugify(water_type_name)+'-'+str(water.id) # mineral-water-15
        water.save()
        
        return super().form_valid(form)
        
    def get_success_message(self, *args, **kwargs):
        return f'{self.object.water_type} has been added to your dashboard'  


class EditType(LoginRequiredMixin, SupplierRoleRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Type
    form_class = WaterTypeForm
    template_name = 'supplier/edit_type.html'
    success_url = reverse_lazy('services')
    login_url = 'login'
    context_object_name = 'water_type_name'
    
    def form_valid(self, form):
        water_type_name = form.cleaned_data['water_type']
        water = form.save(commit=False)
        water.supplier = Supplier.objects.get(user=self.request.user)
        
        water.slug = slugify(water_type_name) + '-' + str(water.id)
        water.save()
        
        return super().form_valid(form)
    
    def get_success_message(self, *args, **kwargs):
        return f'{self.object.water_type}  has been updated successfully'  
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Type, pk=pk)


class DeleteType(LoginRequiredMixin, SupplierRoleRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Type
    template_name = 'supplier/delete_type.html'
    success_url = reverse_lazy('services')
    
    def get_success_message(self, *args, **kwargs):
        return f' {self.object.water_type} has been removed from your dashboard'


class AddProductView(LoginRequiredMixin, SupplierRoleRequiredMixin, CreateView):
    model = Product
    form_class = WaterProductForm
    template_name = 'supplier/add_product.html'
    login_url = 'login'
    
    def form_valid(self, form):
        """
        Assign the supplier before saving the form
        """
        bottle_size = form.cleaned_data['bottle_size']
        bttle_water = form.save(commit=False)
        bttle_water.supplier = Supplier.objects.get(user=self.request.user)
        bttle_water.slug = slugify(bottle_size)
        bttle_water.save()
        
        messages.success(self.request, f'{bottle_size} Water Product has been added successfully')
        return super().form_valid(form)
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        """
        Modify the form fields to show only the type of water that belongs to a specific logged in Supplier
        """
        form.fields['type'].queryset = Type.objects.filter(supplier=Supplier.objects.get(user=self.request.user))
        return form
    
    def get_success_url(self):
        return reverse_lazy('water_by_type', kwargs={'pk': self.object.type.id})


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


class DeleteProduct(LoginRequiredMixin, SupplierRoleRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = Product
    template_name = 'supplier/delete_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the URL to redirect to after canceling
        context['return_url'] = self.request.GET.get('return_url', self.get_success_url())
        return context

    def get_success_url(self):
        return reverse_lazy("water_by_type", kwargs={"pk": self.object.type.pk})

    def get_success_message(self, *args, **kwargs):
        return f'{self.object} has been removed from your dashboard'


class OpeningHoursView(LoginRequiredMixin, FormView, SupplierRoleRequiredMixin, ListView):
    login_url = 'login'
    model = OpeningHour
    form_class = OpeningHourForm
    template_name = 'supplier/opening_hours.html'
    context_object_name = 'opening_hours'
    
    def get_queryset(self):
        self.supplier = get_object_or_404(Supplier, user=self.request.user)
        return OpeningHour.objects.filter(supplier=self.supplier)


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


class RemoveOpeningHoursView(LoginRequiredMixin, View):
    """
    Handle deletion of OpeningHour objects via AJAX requests
    """
    login_url = 'login'
    
    def get(self, request, pk=None):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            response_data = {'status': 'success', 'message': 'Opening hour deleted successfully', 'id':pk}
            print(response_data)
            return JsonResponse(response_data)


class OrderDetailView(SupplierRoleRequiredMixin, View):
    template_name = 'supplier/order_detail.html'

    def get(self, request, order_number):
        cache_key = f'order_detail_{order_number}'
        context = cache.get(cache_key)

        if context:
            print("Retrieving from cache")
        else:
            print("Retrieving from database")
            try:
                order = Order.objects.get(order_number=order_number, is_ordered=True)
                ordered_product = OrderedProduct.objects.filter(order=order, productitem__supplier=get_supplier(request))
                context = {
                    'order': order,
                    'ordered_product': ordered_product,
                    'subtotal': order.get_total_by_supplier()['subtotal'],
                    'tax_data': order.get_total_by_supplier()['tax_dict'],
                    'grand_total': order.get_total_by_supplier()['grand_total'],
                }
                cache.set(cache_key, context, timeout=300)  # Cache timeout of 5 minutes
            except Order.DoesNotExist:
                return redirect('supplier')
        
        return render(request, self.template_name, context)


class MyOrdersView(LoginRequiredMixin, SupplierRoleRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'supplier/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        supplier = Supplier.objects.get(user=self.request.user)
        cache_key = f'my_orders_{self.request.user.username}_{supplier.id}'
        orders = cache.get(cache_key)

        if orders:
            print("Retrieving from cache")
            print(f"Cache key: {cache_key}")
            print(f"Cached orders: {orders}")
        else:
            print("Retrieving from database")
            orders = Order.objects.filter(suppliers__in=[supplier.id], is_ordered=True).order_by('-created_at')
            cache.set(cache_key, orders, timeout=300)  # Cache timeout of 5 minutes

        return orders