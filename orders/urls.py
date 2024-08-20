from django.urls import path
from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('payments/', views.PaymentsView.as_view, name='payments'),
    path('order_complete/', views.OrderCompleteView.as_view(), name='order_complete'),

]