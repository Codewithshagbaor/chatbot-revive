from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import FAQ
import random
from django.http import JsonResponse
from chat.models import Room, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
import string

@login_required(login_url="/login/")
def dashboard(request):
  rooms = Room.objects.all()

  context = {
    'rooms':rooms
  }
  return render(request, "admin/dashboard.html", context)
@login_required
def messages(request):
  rooms = Room.objects.all()

  context = {
    'rooms':rooms
  }
  return render(request, "admin/messages.html", context)