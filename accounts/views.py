"""
Accounts views — Dashboard, Profile, Public Profile.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import ProfileEditForm


@login_required
def dashboard(request):
    """User dashboard with stats overview."""
    user = request.user
    # Gather stats
    active_listings = user.listings.filter(is_active=True).count() if hasattr(user, 'listings') else 0
    active_orders_as_buyer = user.buyer_orders.exclude(status__in=['completed', 'cancelled']).count() if hasattr(user, 'buyer_orders') else 0
    active_orders_as_seller = user.seller_orders.exclude(status__in=['completed', 'cancelled']).count() if hasattr(user, 'seller_orders') else 0
    completed_orders = user.seller_orders.filter(status='completed').count() if hasattr(user, 'seller_orders') else 0
    badges_count = user.user_badges.count() if hasattr(user, 'user_badges') else 0
    resources_uploaded = user.resources.count() if hasattr(user, 'resources') else 0

    # Recent orders
    recent_orders_buyer = user.buyer_orders.order_by('-created_at')[:5] if hasattr(user, 'buyer_orders') else []
    recent_orders_seller = user.seller_orders.order_by('-created_at')[:5] if hasattr(user, 'seller_orders') else []

    context = {
        'active_listings': active_listings,
        'active_orders_as_buyer': active_orders_as_buyer,
        'active_orders_as_seller': active_orders_as_seller,
        'completed_orders': completed_orders,
        'badges_count': badges_count,
        'resources_uploaded': resources_uploaded,
        'recent_orders_buyer': recent_orders_buyer,
        'recent_orders_seller': recent_orders_seller,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_edit(request):
    """Edit own profile."""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:dashboard')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})


def public_profile(request, username):
    """Public profile / portfolio page."""
    user = get_object_or_404(User, username=username)
    listings = user.listings.filter(is_active=True) if hasattr(user, 'listings') else []
    badges = user.user_badges.select_related('badge').all() if hasattr(user, 'user_badges') else []
    reviews_received = user.reviews_received.select_related('reviewer', 'order').order_by('-created_at')[:10] if hasattr(user, 'reviews_received') else []

    context = {
        'profile_user': user,
        'listings': listings,
        'badges': badges,
        'reviews_received': reviews_received,
    }
    return render(request, 'accounts/profile.html', context)
