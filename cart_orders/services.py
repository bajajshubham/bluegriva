"""
Cart logic for anonymous, session-based carts. No login yet, the cart
lives in the visitor's session and will move to a DB-backed cart once
accounts exist.
"""
from catalog.models import Product

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