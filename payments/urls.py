from django.urls import path
from .views import item_buy_view, item_info_view, success_view, cancel_view, item_list_view, order_buy_view, order_info_view

urlpatterns = [
    path('', item_list_view, name='item-list'),
    path('buy/<int:id>/', item_buy_view, name='item_buy'),
    path('item/<int:id>/', item_info_view, name='item_info'),
    path('success/', success_view, name='payment_success'),
    path('cancel/', cancel_view, name='payment_cancel'),
    path('order/<int:id>/buy/', order_buy_view, name='order_buy'),
    path('order/<int:id>', order_info_view, name='order_info'),
]

