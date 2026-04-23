"""
Trust Engine models — Badges and Cryptographic Credentials.
"""
from django.db import models
from django.conf import settings


class Badge(models.Model):
    """Digital skill badge awarded for verified competence."""

    CATEGORY_CHOICES = [
        ('tech', '🖥️ Tech'),
        ('creative', '🎨 Creative'),
        ('business', '📊 Business'),
        ('academic', '📚 Academic'),
        ('language', '🌍 Language'),
        ('special', '⭐ Special'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='special')
    icon = models.CharField(max_length=10, default='🏅', help_text="Emoji icon for the badge")
    criteria = models.TextField(blank=True, help_text="What is required to earn this badge")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    """Badge awarded to a specific user, with cryptographic proof."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_to')
    awarded_at = models.DateTimeField(auto_now_add=True)
    proof_hash = models.CharField(
        max_length=64,
        blank=True,
        help_text="SHA-256 hash for cryptographic proof of competence"
    )

    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-awarded_at']

    def __str__(self):
        return f"{self.user.username} — {self.badge.name}"
