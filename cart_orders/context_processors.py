from . import services


def cart(request):
    """Injects cart_items/cart_total into every template's context."""
    return {
        "cart_items": services.get_cart_items(request),
        "cart_total": services.get_cart_total(request),
    }