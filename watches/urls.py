# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('watches/', views.watch_list, name='watch_list'),
    path('watches/<int:watch_id>/', views.watch_detail, name='watch_detail'),
    path('add_to_cart/<int:watch_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:watch_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:watch_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('order_list/', views.order_list, name='order_list'),
    path('download_invoice/<uuid:order_uuid>/', views.download_invoice, name='download_invoice'),
    path('invoice/<uuid:order_uuid>/', views.invoice, name='invoice'), 
    path('dummy_payment/', views.dummy_payment, name='dummy_payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('contact/', views.contact, name='contact'),
    path('invoice_page',views.invoice_page,name='invoice_page')
]
