"""
Cart and order logic for anonymous, session-based carts. No login yet, the
cart lives in the visitor's session and will move to a DB-backed cart once
accounts exist.
"""
from django.db import transaction
from catalog.models import Product
from .models import Order, OrderItem

SESSION_KEY = "cart"


def _get_session_cart(request):
    """Raw {product_id_str: quantity} dict stored in the session."""
    return request.session.setdefault(SESSION_KEY, {})


def add_item(request, product_id, quantity=1):
    cart = _get_session_cart(request)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + quantity
    request.session.modified = True


def remove_item(request, product_id):
    cart = _get_session_cart(request)
    cart.pop(str(product_id), None)
    request.session.modified = True


def get_cart_items(request):
    """Resolve session {id: qty} into product + quantity + line total."""
    cart = _get_session_cart(request)
    if not cart:
        return []
    products = Product.objects.filter(id__in=cart.keys())
    return [
        {
            "product": product,
            "quantity": cart[str(product.id)],
            "line_total": product.price * cart[str(product.id)],
        }
        for product in products
    ]


def get_cart_total(request):
    return sum(item["line_total"] for item in get_cart_items(request))


def place_order(request, *, guest_name, guest_phone, delivery_address):
    items = get_cart_items(request)
    if not items:
        raise ValueError("Cannot place an order with an empty cart.")

    with transaction.atomic():
        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,   # add this line
            guest_name=guest_name,
            guest_phone=guest_phone,
            delivery_address=delivery_address,
            total_amount=get_cart_total(request),
        )
    """Converts the session cart into a real Order, atomically, then clears the cart."""
    items = get_cart_items(request)
    if not items:
        raise ValueError("Cannot place an order with an empty cart.")

    with transaction.atomic():
        order = Order.objects.create(
            guest_name=guest_name,
            guest_phone=guest_phone,
            delivery_address=delivery_address,
            total_amount=get_cart_total(request),
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )
        request.session[SESSION_KEY] = {}
        request.session.modified = True

    return order

def list_customer_orders(user):
    """Past orders for a logged-in customer, most recent first."""
    return Order.objects.filter(customer=user).order_by("-created_at")