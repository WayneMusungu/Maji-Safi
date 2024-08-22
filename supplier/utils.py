from supplier.models import Supplier


def get_supplier(request):
    supplier = Supplier.objects.get(user=request.user)
    return supplier