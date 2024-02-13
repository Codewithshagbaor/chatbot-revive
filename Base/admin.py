# admin.py
from django.contrib import admin
from .models import FAQ, Profile

@admin.register(FAQ)
class FaqAdmin(admin.ModelAdmin):
  list_display = ('question', 'answer')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'name', 'unique_id')