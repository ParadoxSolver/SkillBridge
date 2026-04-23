from django.contrib import admin
from .models import EscrowTransaction, Wallet


@admin.register(EscrowTransaction)
class EscrowTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'commission_amount', 'net_amount', 'status', 'created_at', 'released_at')
    list_filter = ('status',)
    search_fields = ('order__listing__title',)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_earned', 'total_withdrawn', 'updated_at')
    search_fields = ('user__username',)
