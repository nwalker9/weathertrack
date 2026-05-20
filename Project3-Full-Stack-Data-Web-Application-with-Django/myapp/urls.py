from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('records/', views.record_list, name='record_list'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
    path('records/add/', views.record_create, name='record_create'),
    path('records/<int:pk>/edit/', views.record_update, name='record_update'),
    path('records/<int:pk>/delete/', views.record_delete, name='record_delete'),
    path('analytics/', views.analytics, name='analytics'),
    path('fetch/', views.fetch_data, name='fetch_data'),
    path('players/', views.player_list, name='player_list'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),
    path('players/analytics/', views.player_analytics, name='player_analytics'),
]
