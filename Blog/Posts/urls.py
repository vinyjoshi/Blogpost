from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='post'),
    path('create/', views.post_add, name='add'),
    path('<slug:slug>/', views.post_detail, name='detail'),
    path('<slug:slug>/update/', views.post_update, name='update'),
    path('<slug:slug>/delete/', views.post_delete, name='delete'),    
]