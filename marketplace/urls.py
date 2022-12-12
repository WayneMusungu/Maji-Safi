from django.urls import path
from .import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:supplier_slug>/', views.supplier_detail, name='supplier_detail'),
]