from django.shortcuts import render, get_object_or_404
from catalog.models import Product
from . import services

# Create your views here.
def cart_detail(request):
    """Cart contents — also the fragment returned after add/remove."""
    context = {
        "items": services.get_cart_items(request),
        "total": services.get_cart_total(request),
    }
    return render(request, "cart_orders/_cart_summary.html", context)


def cart_add(request, product_id):
    get_object_or_404(Product, id=product_id, is_active=True)
    services.add_item(request, product_id)
    return cart_detail(request)


def cart_remove(request, product_id):
    services.remove_item(request, product_id)
    return cart_detail(request)