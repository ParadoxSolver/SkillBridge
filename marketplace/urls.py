from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.listing_list, name='list'),
    path('create/', views.listing_create, name='create'),
    path('<int:pk>/', views.listing_detail, name='detail'),
    path('<int:pk>/edit/', views.listing_edit, name='edit'),
    path('<int:pk>/delete/', views.listing_delete, name='delete'),
    path('<int:listing_pk>/order/', views.order_create, name='order_create'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/<int:pk>/deliver/', views.order_deliver, name='order_deliver'),
    path('order/<int:pk>/accept/', views.order_accept, name='order_accept'),
    path('order/<int:pk>/cancel/', views.order_cancel, name='order_cancel'),
    path('order/<int:order_pk>/review/', views.review_create, name='review_create'),
]
