from django.shortcuts import render
from .models import Category
from .services import list_active_products

# Presentational only, no model behind these — plain constants, not database rows.
TRUST_BADGES = [
    {"icon": "droplet", "title": "Triple-washed", "subtitle": "Clean & hygienic"},
    {"icon": "clock", "title": "Saves 20 minutes", "subtitle": "Every meal, every day"},
    {"icon": "leaf", "title": "Farm sourced", "subtitle": "Picked for freshness"},
    {"icon": "truck", "title": "Cold-chain delivery", "subtitle": "Fresh to your door"},
]

PROCESS_STEPS = [
    {"number": "01", "title": "Picked for you", "description": "We source crisp, seasonal produce from trusted farms."},
    {"number": "02", "title": "Washed & cut", "description": "Our trained team cleans and chops every batch in a hygienic prep room."},
    {"number": "03", "title": "Chilled & delivered", "description": "Sealed packs travel cold and arrive ready for your pan, plate or blender."},
]


def product_list(request):
    """Storefront home page: hero, trust badges, real product grid, promo, process steps."""
    category_slug = request.GET.get("category")
    context = {
        "products": list_active_products(category_slug),
        "categories": Category.objects.all(),
        "active_category": category_slug,
        "trust_badges": TRUST_BADGES,
        "process_steps": PROCESS_STEPS,
    }
    return render(request, "catalog/product_list.html", context)