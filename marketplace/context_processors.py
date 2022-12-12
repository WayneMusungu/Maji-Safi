from .models import Cart
from services.models import Product

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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            product = Product.objects.get(pk=item.product.id)
            subtotal += (product.price * item.quantity)
            
        grand_total = subtotal + tax
        # print(subtotal)
        # print(grand_total)
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)