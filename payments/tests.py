from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from unittest.mock import patch
from .models import Item, Order, Discount, Tax

class Tests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item",
            description="Test description",
            price=Decimal('100.00'),
            currency='usd'
        )
        self.client = Client()

    def test_item_info_view(self):
        response = self.client.get(reverse('item_info', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    @patch('payments.views.stripe.checkout.Session.create')
    def test_item_buy_view(self, mock_stripe_create):
        mock_stripe_create.return_value.id = 'test_session'
        response = self.client.get(reverse('item_buy', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 'test_session'})

    def test_order_total_price(self):
        discount = Discount.objects.create(name='10%', percentage=Decimal('10.00'))
        tax = Tax.objects.create(name='5%', percentage=Decimal('5.00'))
        order = Order.objects.create(discount=discount, tax=tax)
        order.items.add(self.item)
        self.assertEqual(order.get_total_price(), Decimal('9450'))
