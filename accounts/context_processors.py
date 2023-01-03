from .models import UserProfile
from supplier.models import Supplier
from django.conf import settings
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


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


"""
Create a function that returns the GOOGLE API KEY
"""

def get_google_api(request):
    return{'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}

"""
Create a Function that gets the client id and access it in the base template
"""
def get_paypal_client_id(request):
    return{'PAYPAL_CLIENT_ID':settings.PAYPAL_CLIENT_ID}