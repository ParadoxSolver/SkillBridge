from django.urls import path
from . import views

app_name = 'trustengine'

urlpatterns = [
    path('badges/', views.badge_gallery, name='badges'),
    path('badges/<int:pk>/', views.badge_detail, name='badge_detail'),
    path('badges/user/<str:username>/', views.user_badges, name='user_badges'),
]
