"""
Escrow models — Transaction management and Wallets.
"""
from django.db import models
from django.conf import settings


class EscrowTransaction(models.Model):
    """Escrow transaction holding payment for an order."""

    STATUS_CHOICES = [
        ('held', 'Held in Escrow'),
        ('released', 'Released to Seller'),
        ('refunded', 'Refunded to Buyer'),
        ('disputed', 'Under Dispute'),
    ]

    order = models.ForeignKey('marketplace.Order', on_delete=models.CASCADE, related_name='escrow_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.15)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Amount seller receives after commission")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='held')
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Escrow #{self.pk} — ₹{self.amount} ({self.get_status_display()})"


class Wallet(models.Model):
    """User wallet for tracking balance."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet — ₹{self.balance}"
