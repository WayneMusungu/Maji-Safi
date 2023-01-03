from django.http import HttpResponse
from django.shortcuts import render, redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import Order
import simplejson as json
from .utils import generate_order_number

# Create your views here.

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    # If cart count is 0 redirect user to the market place page
    if cart_count <= 0:
        return redirect('marketplace')
    
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == 'POST': 
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.county = form.cleaned_data['county']
            order.town = form.cleaned_data['town']
            order.pin_code = form.cleaned_data['pin_code']      
            order.user = request.user   
            order.total = grand_total
            order.tax_data = json.dumps(tax_data) # convert the tax data into json format
            order.total_tax = total_tax    
            order.payment_method = request.POST['payment_method'] 
            order.save() #order id/pk is generated
            order.order_number = generate_order_number(order.id)
            order.save()
            context = {
                'order': order,
                'cart_items': cart_items
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)
    
    print(subtotal,total_tax,grand_total,tax_data)
    return render(request, 'orders/place_order.html')


def payments(request):
    return HttpResponse('Payments view')
