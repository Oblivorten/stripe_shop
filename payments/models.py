from django.db import models
from decimal import Decimal, ROUND_HALF_UP

class Item(models.Model):
    choices = [
        ('usd', 'USD'),
        ('rub', 'RUB'),
        ('eur', 'EUR'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=choices, default='rub')

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    def get_total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total -= total * (self.discount.percentage / Decimal('100'))
        if self.tax:
            total += total * (self.tax.percentage / Decimal('100'))
        return (total * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)