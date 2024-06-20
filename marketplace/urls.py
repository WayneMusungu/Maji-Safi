from django.urls import path
from .import views

urlpatterns = [
    path('', views.MarketPlaceView.as_view(), name='marketplace'),
    path('<slug:supplier_slug>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    
    
    # ADD TO CART
    
    path('add_to_cart/<int:product_id>/', views.AddCartView.as_view(), name='add_to_cart'),
    
    
    # DECREASE CART
    
    path('decrease_cart/<int:product_id>/', views.DecreaseCartView.as_view(), name='decrease_cart'),
    
    
    # DELETE CART
    
    path('delete_cart/<int:cart_id>/', views.DeleteCartView.as_view(), name='delete_cart')
    
    
   

    
]