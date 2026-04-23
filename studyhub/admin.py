from django.contrib import admin
from .models import Resource, ResourceVote


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'category', 'subject', 'upvotes', 'download_count', 'is_verified', 'created_at')
    list_filter = ('category', 'is_verified')
    search_fields = ('title', 'description', 'subject', 'tags')
    list_editable = ('is_verified',)


@admin.register(ResourceVote)
class ResourceVoteAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'vote_type', 'created_at')
