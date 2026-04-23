"""
Marketplace views — Browse, Create, Order, Review.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from .models import ServiceListing, Order, Review
from .forms import ServiceListingForm, OrderForm, ReviewForm


def listing_list(request):
    """Browse/search marketplace listings."""
    listings = ServiceListing.objects.filter(is_active=True).select_related('seller')

    # Search
    query = request.GET.get('q', '')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query) |
            Q(seller__username__icontains=query)
        )

    # Category filter
    category = request.GET.get('category', '')
    if category:
        listings = listings.filter(category=category)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        listings = listings.order_by('price')
    elif sort == 'price_high':
        listings = listings.order_by('-price')
    elif sort == 'rating':
        listings = listings.annotate(avg_rating=Avg('orders__review__rating')).order_by('-avg_rating')
    else:
        listings = listings.order_by('-created_at')

    categories = ServiceListing.CATEGORY_CHOICES

    context = {
        'listings': listings,
        'query': query,
        'category': category,
        'sort': sort,
        'categories': categories,
    }
    return render(request, 'marketplace/list.html', context)


def listing_detail(request, pk):
    """View a single service listing."""
    listing = get_object_or_404(ServiceListing.objects.select_related('seller'), pk=pk)
    reviews = Review.objects.filter(order__listing=listing, order__status='completed').select_related('reviewer').order_by('-created_at')
    order_form = OrderForm()

    context = {
        'listing': listing,
        'reviews': reviews,
        'order_form': order_form,
    }
    return render(request, 'marketplace/detail.html', context)


@login_required
def listing_create(request):
    """Create a new service listing."""
    if request.method == 'POST':
        form = ServiceListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            messages.success(request, 'Your service has been listed! 🎉')
            return redirect('marketplace:detail', pk=listing.pk)
    else:
        form = ServiceListingForm()

    return render(request, 'marketplace/create.html', {'form': form})


@login_required
def listing_edit(request, pk):
    """Edit an existing listing."""
    listing = get_object_or_404(ServiceListing, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ServiceListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('marketplace:detail', pk=listing.pk)
    else:
        form = ServiceListingForm(instance=listing)

    return render(request, 'marketplace/create.html', {'form': form, 'editing': True})


@login_required
def listing_delete(request, pk):
    """Delete a listing."""
    listing = get_object_or_404(ServiceListing, pk=pk, seller=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted.')
        return redirect('marketplace:list')
    return render(request, 'marketplace/confirm_delete.html', {'listing': listing})


@login_required
def order_create(request, listing_pk):
    """Place an order for a listing."""
    listing = get_object_or_404(ServiceListing, pk=listing_pk, is_active=True)

    if listing.seller == request.user:
        messages.error(request, "You can't order your own service!")
        return redirect('marketplace:detail', pk=listing.pk)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.listing = listing
            order.buyer = request.user
            order.seller = listing.seller
            order.total_price = listing.price
            order.save()

            # Create escrow transaction
            from escrow.models import EscrowTransaction
            from django.conf import settings as django_settings
            commission_rate = django_settings.ESCROW_COMMISSION_RATE
            commission = order.total_price * commission_rate
            EscrowTransaction.objects.create(
                order=order,
                amount=order.total_price,
                commission_rate=commission_rate,
                commission_amount=commission,
                net_amount=order.total_price - commission,
                status='held',
            )

            messages.success(request, f'Order placed! ₹{order.total_price} held in escrow. 🔒')
            return redirect('marketplace:order_detail', pk=order.pk)

    return redirect('marketplace:detail', pk=listing.pk)


@login_required
def order_detail(request, pk):
    """View order details."""
    order = get_object_or_404(
        Order.objects.select_related('listing', 'buyer', 'seller'),
        pk=pk
    )
    # Only buyer or seller can view
    if request.user not in (order.buyer, order.seller):
        messages.error(request, "You don't have access to this order.")
        return redirect('marketplace:list')

    escrow = order.escrow_transactions.first() if hasattr(order, 'escrow_transactions') else None
    review_form = ReviewForm()
    has_review = hasattr(order, 'review')

    context = {
        'order': order,
        'escrow': escrow,
        'review_form': review_form,
        'has_review': has_review,
    }
    return render(request, 'marketplace/order_detail.html', context)


@login_required
def order_deliver(request, pk):
    """Seller marks order as delivered."""
    order = get_object_or_404(Order, pk=pk, seller=request.user)
    if order.status in ('pending', 'in_progress'):
        order.status = 'delivered'
        order.delivered_at = timezone.now()
        order.save()
        messages.success(request, 'Order marked as delivered! Waiting for buyer approval. ✅')
    return redirect('marketplace:order_detail', pk=order.pk)


@login_required
def order_accept(request, pk):
    """Buyer accepts delivery and releases escrow."""
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    if order.status == 'delivered':
        order.status = 'completed'
        order.completed_at = timezone.now()
        order.save()

        # Release escrow
        escrow = order.escrow_transactions.first()
        if escrow and escrow.status == 'held':
            escrow.status = 'released'
            escrow.released_at = timezone.now()
            escrow.save()

            # Update seller earnings
            order.seller.total_earnings += escrow.net_amount
            order.seller.save()

            # Update buyer spending
            order.buyer.total_spent += escrow.amount
            order.buyer.save()

        # Auto-award badge for completed work
        from trustengine.models import Badge, UserBadge
        import hashlib
        badge, _ = Badge.objects.get_or_create(
            name=f"{order.listing.get_category_display()} Expert",
            defaults={
                'description': f'Completed a {order.listing.get_category_display()} project successfully.',
                'category': order.listing.category,
            }
        )
        proof = f"{order.pk}-{order.seller.pk}-{order.completed_at.isoformat()}"
        proof_hash = hashlib.sha256(proof.encode()).hexdigest()
        UserBadge.objects.get_or_create(
            user=order.seller,
            badge=badge,
            defaults={'proof_hash': proof_hash}
        )

        messages.success(request, 'Order completed! Payment released to seller. 🎉')
    return redirect('marketplace:order_detail', pk=order.pk)


@login_required
def order_cancel(request, pk):
    """Cancel an order (buyer only, only if pending)."""
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()

        # Refund escrow
        escrow = order.escrow_transactions.first()
        if escrow and escrow.status == 'held':
            escrow.status = 'refunded'
            escrow.save()

        messages.success(request, 'Order cancelled and escrow refunded.')
    return redirect('marketplace:order_detail', pk=order.pk)


@login_required
def review_create(request, order_pk):
    """Submit a review for a completed order."""
    order = get_object_or_404(Order, pk=order_pk, buyer=request.user, status='completed')

    if hasattr(order, 'review'):
        messages.info(request, 'You have already reviewed this order.')
        return redirect('marketplace:order_detail', pk=order.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.reviewer = request.user
            review.reviewee = order.seller
            review.save()

            # Update seller trust score
            avg = Review.objects.filter(reviewee=order.seller).aggregate(avg=Avg('rating'))['avg']
            order.seller.trust_score = round(avg, 2) if avg else 0
            order.seller.save()

            messages.success(request, 'Review submitted! Thank you. ⭐')
            return redirect('marketplace:order_detail', pk=order.pk)

    return redirect('marketplace:order_detail', pk=order.pk)
