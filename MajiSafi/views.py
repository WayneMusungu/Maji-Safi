from django.views.generic import ListView
from supplier.models import Supplier


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'suppliers'
    
    def get_queryset(self):
        return Supplier.objects.filter(is_approved=True, user__is_active=True)[:10]

