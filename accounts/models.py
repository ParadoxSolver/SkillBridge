"""
Custom User model for SkillBridge.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """Extended user with student profile, skills, and trust scoring."""

    # College verification
    college_email = models.EmailField(blank=True, help_text="Official college email for verification")
    college_name = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False, help_text="College ID verified")

    # Profile
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")

    # Trust & earnings
    trust_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.username})

    @property
    def skills_list(self):
        """Return skills as a list."""
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []

    @property
    def completed_orders_count(self):
        return self.seller_orders.filter(status='completed').count()

    @property
    def active_listings_count(self):
        return self.listings.filter(is_active=True).count()
