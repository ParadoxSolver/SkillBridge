"""
Study Hub models — Academic Resources with peer verification.
"""
from django.db import models
from django.conf import settings
from django.urls import reverse


class Resource(models.Model):
    """An academic resource uploaded by a student."""

    CATEGORY_CHOICES = [
        ('lecture_notes', '📝 Lecture Notes'),
        ('past_papers', '📄 Past Papers'),
        ('mind_maps', '🧠 Mind Maps'),
        ('project_templates', '📋 Project Templates'),
        ('research_guides', '🔬 Research Guides'),
    ]

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=100)
    course = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags")
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False, help_text="Peer-verified for accuracy")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.subject}"

    def get_absolute_url(self):
        return reverse('studyhub:detail', kwargs={'pk': self.pk})

    @property
    def net_votes(self):
        return self.upvotes - self.downvotes

    @property
    def tags_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []


class ResourceVote(models.Model):
    """Track individual user votes on resources."""
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resource', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.vote_type} on {self.resource.title}"
