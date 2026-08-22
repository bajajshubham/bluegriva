"""
OTP login logic. Dev-only for now: the code is printed to the console instead
of a real SMS gateway, that integration is a separate later step.
"""
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import login as django_login
from .models import User, PhoneOTP

OTP_VALID_MINUTES = 5
RESEND_COOLDOWN_SECONDS = 30


def request_otp(phone):
    """Generates and 'sends' a 6-digit OTP. Enforces a resend cooldown."""
    recent = PhoneOTP.objects.filter(phone=phone).order_by("-created_at").first()
    if recent and (timezone.now() - recent.created_at).total_seconds() < RESEND_COOLDOWN_SECONDS:
        raise ValueError("Please wait before requesting another code.")

    code = f"{random.randint(0, 999999):06d}"
    PhoneOTP.objects.create(phone=phone, code=code)
    print(f"[DEV] OTP for {phone}: {code}")  # stand-in for a real SMS gateway
    return code


def verify_otp(request, phone, code):
    """Validates the code, logs the user in (creating the account on first login)."""
    cutoff = timezone.now() - timedelta(minutes=OTP_VALID_MINUTES)
    otp = PhoneOTP.objects.filter(
        phone=phone, code=code, is_used=False, created_at__gte=cutoff
    ).order_by("-created_at").first()

    if not otp:
        raise ValueError("Invalid or expired code.")

    otp.is_used = True
    otp.save(update_fields=["is_used"])

    user, _ = User.objects.get_or_create(phone=phone)
    django_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return user