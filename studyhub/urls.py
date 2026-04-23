from django.urls import path
from . import views

app_name = 'studyhub'

urlpatterns = [
    path('', views.resource_list, name='list'),
    path('upload/', views.resource_upload, name='upload'),
    path('<int:pk>/', views.resource_detail, name='detail'),
    path('<int:pk>/download/', views.resource_download, name='download'),
    path('<int:pk>/vote/<str:vote_type>/', views.resource_vote, name='vote'),
]
