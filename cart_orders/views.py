from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Product
from . import services
from .models import Order


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


def checkout(request):
    items = services.get_cart_items(request)
    if request.method == "POST" and items:
        order = services.place_order(
            request,
            guest_name=request.POST["guest_name"],
            guest_phone=request.POST["guest_phone"],
            delivery_address=request.POST["delivery_address"],
        )
        return redirect("cart_orders:order_confirmation", order_id=order.id)

    return render(request, "cart_orders/checkout.html", {
        "items": items,
        "total": services.get_cart_total(request),
    })


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "cart_orders/order_confirmation.html", {"order": order})