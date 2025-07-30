from django.shortcuts import render, get_object_or_404
from .models import Item, Order
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def item_buy_view(request, id):
    item = get_object_or_404(Item, id=id)
    line_items = [{
        'price_data': {
            'currency': item.currency,
            'product_data': {
                'name': item.name,
            },
            'unit_amount': int(item.price * 100),
        },
        'quantity': 1,
    }]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    )
    return JsonResponse({'id': session.id})

def item_info_view(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'payments/item_info.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

def success_view(request):
    return render(request, 'payments/success.html')

def cancel_view(request):
    return render(request, 'payments/cancel.html')

def item_list_view(request):
    items = Item.objects.all()
    return render(request, 'payments/item_list.html', {'items': items})


def order_buy_view(request, id):
    order = get_object_or_404(Order, id=id)
    tax_rates = []
    if order.tax:
        tax_rate = stripe.TaxRate.create(
            display_name=order.tax.name,
            percentage=float(order.tax.percentage),
            inclusive=False
        )
        tax_rates.append(tax_rate.id)
    discounts = []
    if order.discount:
        coupon = stripe.Coupon.create(
            percent_off=float(order.discount.percentage),
            duration='once'
        )
        promo = stripe.PromotionCode.create(coupon=coupon.id)
        discounts.append({'promotion_code': promo.id})
    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name},
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
            'tax_rates': tax_rates,
        })
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        discounts=discounts,
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel'))
    )
    return JsonResponse({'id': session.id})

def order_info_view(request, id):
    order = get_object_or_404(Order, id=id)
    total_price = order.get_total_price() / 100
    return render(request, 'payments/order_info.html', {
        'order': order,
        'total_price': total_price,
        'total_price_raw': order.get_total_price(),
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })
