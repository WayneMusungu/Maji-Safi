from .models import Cart
from services.models import Product
from.models import Tax

"""
Display the cart_count dynamically
"""
def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            """
            If there is cart items, then loop through it and add the quantities
            """
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
               cart_count = 0 
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            product = Product.objects.get(pk=item.product.id)
            subtotal += (product.price * item.quantity)
            
        get_tax = Tax.objects.filter(is_active=True)
        print(get_tax)
        
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal)/100, 2)
            tax_dict.update({tax_type: {str(tax_percentage) : tax_amount}})
        
        tax = sum(x for key in tax_dict.values() for x in key.values())
        grand_total = subtotal + tax
    # print(tax_dict)
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total, tax_dict=tax_dict)
    
      
    