from django.shortcuts import render
from catalog.services import list_active_products, list_categories

# Presentational content, no model behind it — plain constants, not database rows.
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


def home(request):
    """Storefront home page: hero, trust badges, product grid, promo, process steps.
    core assembles the page; catalog owns the product data behind it."""
    category_slug = request.GET.get("category")
    search = request.GET.get("q", "").strip()
    context = {
        "products": list_active_products(category_slug, search),
        "categories": list_categories(),
        "active_category": category_slug,
        "trust_badges": TRUST_BADGES,
        "process_steps": PROCESS_STEPS,
    }
    return render(request, "core/home.html", context)