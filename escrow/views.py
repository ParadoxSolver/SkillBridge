"""
Escrow views — Wallet dashboard, transaction history.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import EscrowTransaction, Wallet


@login_required
def wallet_dashboard(request):
    """View wallet balance and transaction history."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    # Transactions where user is buyer or seller
    transactions = EscrowTransaction.objects.filter(
        order__buyer=request.user
    ) | EscrowTransaction.objects.filter(
        order__seller=request.user
    )
    transactions = transactions.select_related('order', 'order__listing').order_by('-created_at')

    context = {
        'wallet': wallet,
        'transactions': transactions,
    }
    return render(request, 'escrow/wallet.html', context)
