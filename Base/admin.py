# admin.py
from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FaqAdmin(admin.ModelAdmin):
  list_display = ('question', 'answer')
