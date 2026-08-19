from django.shortcuts import render

# Create your views here.
def home(request):
    """Placeholder page — proves Django + Tailwind + HTMX are wired up."""
    return render(request, 'core/home.html')