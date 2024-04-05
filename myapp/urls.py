from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('read_all_recipes/', views.read_all_recipes, name='read_all_recipes'),
    path('recipe_detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('search/', views.search, name='search'),
]
