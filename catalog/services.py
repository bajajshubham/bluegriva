"""Query/business logic for catalog. views.py (HTMX) and, later, api/v1/ (JSON)
both call these functions — never the other way around."""
from .models import Category, Product


def list_active_products(category_slug=None):
    """Active products for the storefront grid, optionally filtered by category."""
    products = Product.objects.filter(is_active=True).select_related("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)
    return products

def list_categories():
    return Category.objects.all()