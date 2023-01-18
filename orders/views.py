from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from marketplace.models import Cart, Tax
from marketplace.context_processors import get_cart_amounts
from services.models import Product
from .forms import OrderForm
from .models import Order, OrderedProduct, Payment
import simplejson as json
from .utils import generate_order_number, order_total_by_supplier
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    # If cart count is 0 redirect user to the market place page
    if cart_count <= 0:
        return redirect('marketplace')
    
    
    suppliers_ids = []
    for i in cart_items:
        if i.product.supplier.id not in suppliers_ids:
            suppliers_ids.append(i.product.supplier.id)
    # print(suppliers_ids)
    
    #{'supplier_id':{'subtotal':{'tax_type': 'tax_amount'}}}
    get_tax = Tax.objects.filter(is_active=True)
    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        product = Product.objects.get(pk=i.product.id, supplier_id__in=suppliers_ids) # show the individual supplier productitem
        s_id = product.supplier.id
        if s_id in k:
            subtotal = k[s_id]
            subtotal += (product.price * i.quantity)
            k[s_id] = subtotal
        else:
            subtotal = (product.price * i.quantity)
            k[s_id] = subtotal
        #  print(k)
            # Calculate the tax data
        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal)/100, 2)
            tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}})
        # print(tax_dict)
        
        # Construct total_data
        total_data.update({product.supplier.id: {str(subtotal): str(tax_dict)}})
    print(total_data)
    # print(product, product.supplier.id)
    
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
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax    
            order.payment_method = request.POST['payment_method'] 
            order.save() #order id/pk is generated
            order.order_number = generate_order_number(order.id)
            order.suppliers.add(*suppliers_ids) #Recursively add the data to ManyToMany Field
            order.save()
            context = {
                'order': order,
                'cart_items': cart_items
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)
    
    # print(subtotal,total_tax,grand_total,tax_data)
    return render(request, 'orders/place_order.html')


@login_required(login_url='login')
def payments(request):
    # Check if the request is ajax or not
    if request.headers.get('x-requested-with')  == 'XMLHttpRequest' and request.method == 'POST':
    
        # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number = request.POST.get('order_number') #order_number is coming from ajax which is request.post in place_order.html
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        # print(order_number,transaction_id,payment_method,status)
        
        order = Order.objects.get(user=request.user, order_number=order_number)
        
        
            #Create payment Object and initialize it
        payment = Payment(
            user = request.user,
            transaction_id= transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status,  
        ) 
        payment.save()
        
        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()
        # return HttpResponse('Saved!')
        
        # MOVE THE CART ITEMS TO ORDERED PRODUCT MODEL
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_product = OrderedProduct()
            ordered_product.order = order
            ordered_product.payment = payment
            ordered_product.user = request.user
            ordered_product.productitem = item.product
            ordered_product.quantity = item.quantity
            ordered_product.price = item.product.price
            ordered_product.amount = item.product.price * item.quantity # total amount
            ordered_product.save()
            
        # return HttpResponse('Saved ordered food')
        
        # SEND ORDER CONFIRMATION EMAIL TO THE CUSTOMER
        subject = 'Thank you for making an order'
        email_template = 'orders/emails/order_confirmation_email.html'
        
        # Create access to Ordered Products and display it on order_confirmation_email.html
        ordered_product = OrderedProduct.objects.filter(order=order)
        
        customer_subtotal = 0
        for item in ordered_product:
            customer_subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        
        
        context = {
            'user': request.user,
            'order': order,
            # The to_email need not to be the logged in user email address it can be billing email address
            'to_email': order.email,
            'ordered_product':ordered_product,
            'domain': get_current_site(request),
            'customer_subtotal': customer_subtotal,
            'tax_data': tax_data,
            
        }
        send_notification(subject, email_template, context)
        # return HttpResponse('Data Saved and email sent')
        
        
        # SEND ORDER RECEIVED EMAIL TO THE SUPPLIER
        subject = 'You have received a new order'
        email_template = 'orders/emails/new_order_received_email.html'
        to_emails = []
        for i in cart_items:
            if i.product.supplier.user.email not in to_emails:
                to_emails.append(i.product.supplier.user.email)
                
                # Get the Supplier's Specific Ordered Product
                ordered_product_to_supplier = OrderedProduct.objects.filter(order=order, productitem__supplier=i.product.supplier)
                print(ordered_product_to_supplier)
                
                
                # print('to_emails=>',to_emails)
                context = {
                    'order': order,
                    # to_email can be a list, and send the email to the list of suppliers
                    'to_email':i.product.supplier.user.email,
                    'ordered_product_to_supplier':ordered_product_to_supplier,
                    'supplier_subtotal':order_total_by_supplier(order, i.product.supplier.id)['subtotal'],
                    'tax_data':order_total_by_supplier(order, i.product.supplier.id)['tax_dict'],
                    'supplier_grand_total':order_total_by_supplier(order, i.product.supplier.id)['grand_total'],
                }
                send_notification(subject, email_template, context)
        # return HttpResponse('Data Saved and email sent')
        
        
        # CLEAR CART IF THE PAYMENT IS SUCCESS
        # cart_items.delete()
        # return HttpResponse('Data Saved and email sent')
       
        # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id
        }
        return JsonResponse(response)
    return HttpResponse('Payments view')


@login_required(login_url='login')

def order_complete(request):
    # Get the response from place_order url parameter and fetch order and ordered product:
        # window.location.href = order_complete + '?order_no='+response.order_number+'&trans_id='+response.transaction_id
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_product = OrderedProduct.objects.filter(order=order)
        
        subtotal = 0
        for item in ordered_product:
            subtotal += (item.price * item.quantity)
            
        tax_data = json.loads(order.tax_data)
        # print(tax_data)
        
        context = {
            'order': order,
            'ordered_product': ordered_product,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'orders/order_complete.html', context)

    except:
        return redirect('home')
