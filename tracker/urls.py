from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('weight/', views.weight_tracker, name='weight_tracker'),
    path('exercise/', views.exercise_tracker, name='exercise_tracker'),
    path('nutrition/', views.nutrition_tracker, name='nutrition_tracker'),
    path('sleep/', views.sleep_tracker, name='sleep_tracker'),
    path('water/', views.water_tracker, name='water_tracker'),
    path('goals/', views.goals, name='goals'),
    path('mood/', views.mood_tracker, name='mood_tracker'),
    path('profile/', views.profile, name='profile'),
    path('analytics/', views.analytics, name='analytics'),
    path('quick-add/', views.quick_add, name='quick_add'),
    
    # CRUD operations
    path('edit/<str:model_name>/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<str:model_name>/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    
    # API endpoints
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
]
