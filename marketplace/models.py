"""
Marketplace models — Service Listings, Orders, Milestones, Reviews.
"""
from django.db import models
from django.conf import settings
from django.urls import reverse


class ServiceListing(models.Model):
    """A service listed by a student on the marketplace."""

    CATEGORY_CHOICES = [
        ('tech', '🖥️ Tech'),
        ('creative', '🎨 Creative'),
        ('business', '📊 Business'),
        ('academic', '📚 Academic'),
        ('language', '🌍 Language'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days = models.PositiveIntegerField(default=3, help_text="Expected delivery in days")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.seller.username}"

    def get_absolute_url(self):
        return reverse('marketplace:detail', kwargs={'pk': self.pk})

    @property
    def tags_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []

    @property
    def review_count(self):
        return Review.objects.filter(order__listing=self, order__status='completed').count()

    @property
    def average_rating(self):
        reviews = Review.objects.filter(order__listing=self, order__status='completed')
        if reviews.exists():
            return round(reviews.aggregate(avg=models.Avg('rating'))['avg'], 1)
        return 0


class Order(models.Model):
    """An order placed by a buyer for a service listing."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('disputed', 'Disputed'),
        ('cancelled', 'Cancelled'),
    ]

    listing = models.ForeignKey(ServiceListing, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_orders')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField(blank=True, help_text="Buyer's project requirements")
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} — {self.listing.title}"

    def get_absolute_url(self):
        return reverse('marketplace:order_detail', kwargs={'pk': self.pk})


class OrderMilestone(models.Model):
    """Milestones within an order for milestone-based project management."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({'✓' if self.is_completed else '○'})"


class Review(models.Model):
    """Review submitted after order completion."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.reviewer.username} — {self.rating}★"
