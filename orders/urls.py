from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart'),
    path('cart/update/<str:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<str:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('pay/<uuid:token>/', views.payment_mock, name='pay'),
    path('done/<uuid:token>/', views.order_done, name='done'),
]
