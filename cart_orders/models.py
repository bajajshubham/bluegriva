from django.db import models
from catalog.models import Product


class Order(models.Model):
    """A placed order. No account yet, guest details are captured at checkout."""

    STATUS_CHOICES = [
        ("placed", "Placed"),
        ("confirmed", "Confirmed"),
        ("packed", "Packed"),
        ("out_for_delivery", "Out for delivery"),
        ("delivered", "Delivered"),
    ]
    PAYMENT_CHOICES = [("cod", "Cash on Delivery")]  # Razorpay added in a later step

    guest_name = models.CharField(max_length=100)
    guest_phone = models.CharField(max_length=15)
    delivery_address = models.TextField()
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cod")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} — {self.guest_name}"


class OrderItem(models.Model):
    """One product line within an order. Price is snapshotted at order time,
    so a later price change on the product doesn't rewrite past orders."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def line_total(self):
        return self.price * self.quantity