from supplier.models import Supplier
"""
Make data accessible to all HTML files

Create a function that takes request as an argument and returns a dictionary that gets added to the request
"""
#Register it to settings TEMPLATES

def get_supplier(request):
    try:
        supplier = Supplier.objects.get(user=request.user)
    except:
        supplier = None
    return dict(supplier=supplier)