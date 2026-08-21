from django.urls import path
from . import views

app_name = "cart_orders"

urlpatterns = [
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
]