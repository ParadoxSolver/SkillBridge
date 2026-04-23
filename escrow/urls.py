from django.urls import path
from . import views

app_name = 'escrow'

urlpatterns = [
    path('wallet/', views.wallet_dashboard, name='wallet'),
]
