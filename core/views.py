"""
Core views — Landing page with dynamic stats.
"""
from django.shortcuts import render
from accounts.models import User
from marketplace.models import ServiceListing
from studyhub.models import Resource


def landing(request):
    """Landing page with live platform stats."""
    context = {
        'student_count': User.objects.filter(is_active=True, is_staff=False).count(),
        'listing_count': ServiceListing.objects.filter(is_active=True).count(),
        'resource_count': Resource.objects.count(),
    }
    return render(request, 'core/index.html', context)
