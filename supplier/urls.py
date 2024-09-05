from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.SupplierDashboardView.as_view(), name='supplier'),
    path('profile/', views.SupplierProfileView.as_view(), name='supplierProfile'),
    path('services/', views.Services.as_view() ,name='services'),
    path('services/type/<int:pk>/', views.WaterByTypeView.as_view() ,name='water_by_type'),
    
    
    # SERVICES TYPE CRUD
    path('services/type/add/', views.AddType.as_view(), name ='add_type'),
    path('services/type/edit/<int:pk>/', views.EditType.as_view() ,name='edit_type'),
    path('services/type/delete/<int:pk>/', views.DeleteType.as_view() ,name='delete_type'),
    
    
    # SERVICES PRODUCT CRUD
    path('services/product/add/', views.AddProductView.as_view(), name ='add_product'),
    path('services/product/edit/<int:pk>/', views.EditProductView.as_view() ,name='edit_product'),
    path('services/product/ delete_product/<int:pk>/', views.DeleteProduct.as_view() ,name='delete_product'),
    
    
    # OPENING HOUR CRUD
    path('opening-hours/', views.OpeningHoursView.as_view(), name='opening_hours'),
    path('opening-hours/add/', views.AddOpeningHoursView.as_view(), name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.RemoveOpeningHoursView.as_view(), name='remove_opening_hours'),
    
    
    # ORDER DETAIL
    path('order_detail/<int:order_number>/', views.OrderDetailView.as_view(), name='supplier_order_detail'),
    path('my_orders/', views.MyOrdersView.as_view(), name='supplier_my_orders'), 


    # CHART DATA
    path('water-type-chart/', views.WaterTypeOrderChartView.as_view(), name='water_type_chart_data'),
]