from django.contrib import admin
from .models import ServiceListing, Order, OrderMilestone, Review


@admin.register(ServiceListing)
class ServiceListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'is_active', 'is_featured', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('title', 'description', 'tags', 'seller__username')
    list_editable = ('is_active', 'is_featured')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'buyer', 'seller', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('listing__title', 'buyer__username', 'seller__username')


@admin.register(OrderMilestone)
class OrderMilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_completed')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'reviewer', 'reviewee', 'rating', 'created_at')
    list_filter = ('rating',)
