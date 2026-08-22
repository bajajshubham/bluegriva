from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("account/login/", views.otp_request, name="login"),
    path("account/login/verify/", views.otp_verify, name="verify"),
    path("account/logout/", views.logout_view, name="logout"),
    path("account/orders/", views.order_history, name="order_history"),
]