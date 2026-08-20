from django.shortcuts import render
from .models import Category
from .services import list_active_products

# Create your views here.
def product_list(request):
    """Storefront grid — matches the Figma 'storefront' frame."""
    category_slug = request.GET.get("category")
    context = {
        "products": list_active_products(category_slug),
        "categories": Category.objects.all(),
        "active_category": category_slug,
    }
    return render(request, "catalog/product_list.html", context)