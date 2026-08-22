from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from . import services


def otp_request(request):
    error = None
    if request.method == "POST":
        phone = request.POST["phone"]
        try:
            services.request_otp(phone)
            return redirect(f"/account/login/verify/?phone={phone}")
        except ValueError as e:
            error = str(e)
    return render(request, "accounts/login_request.html", {"error": error})


def otp_verify(request):
    phone = request.GET.get("phone") or request.POST.get("phone")
    error = None
    if request.method == "POST":
        try:
            services.verify_otp(request, phone, request.POST["code"])
            return redirect("core:home")
        except ValueError as e:
            error = str(e)
    return render(request, "accounts/login_verify.html", {"phone": phone, "error": error})


def logout_view(request):
    django_logout(request)
    return redirect("core:home")