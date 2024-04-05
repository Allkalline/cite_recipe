from django.contrib import admin
from .models import Recipe, UserProfile, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
