from django.shortcuts import render

# Create your views here.

def supplierProfile(request):
    return render(request, 'supplier/supplierProfile.html')
