"""
Trust Engine views — Badge gallery and user badge portfolio.
"""
from django.shortcuts import render, get_object_or_404
from .models import Badge, UserBadge
from accounts.models import User


def badge_gallery(request):
    """View all available badges."""
    badges = Badge.objects.all()

    # Filter by category
    category = request.GET.get('category', '')
    if category:
        badges = badges.filter(category=category)

    context = {
        'badges': badges,
        'category': category,
        'categories': Badge.CATEGORY_CHOICES,
    }
    return render(request, 'trustengine/badges.html', context)


def badge_detail(request, pk):
    """View badge details and who has earned it."""
    badge = get_object_or_404(Badge, pk=pk)
    awarded = UserBadge.objects.filter(badge=badge).select_related('user')

    context = {
        'badge': badge,
        'awarded': awarded,
    }
    return render(request, 'trustengine/badge_detail.html', context)


def user_badges(request, username):
    """View a user's badge portfolio."""
    user = get_object_or_404(User, username=username)
    badges = UserBadge.objects.filter(user=user).select_related('badge')

    context = {
        'profile_user': user,
        'badges': badges,
    }
    return render(request, 'trustengine/user_badges.html', context)
