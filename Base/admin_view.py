from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import FAQ, Profile
import random
from django.http import JsonResponse
from chat.models import Room, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse  
import string
@login_required(login_url="/login/")
def dashboard(request):
  rooms = Room.objects.all()[:8]
  room_count = Room.objects.all().count()
  faqs_count = FAQ.objects.all().count()
  users = Profile.objects.all().count()

  context = {
    'rooms':rooms,
    'room_count':room_count,
    'faqs_count':faqs_count,
    'users':users
  }
  return render(request, "admin/dashboard.html", context)
@login_required(login_url="/login/")
def messages(request):
  all_rooms = Room.objects.all()
  rooms_per_page = 10
  page = request.GET.get('page', 1)
  paginator = Paginator(all_rooms, rooms_per_page)
  try:
      rooms = paginator.page(page)
  except PageNotAnInteger:
     rooms = paginator.page(1)
  except EmptyPage:
        rooms = paginator.page(paginator.num_pages)

    # Calculate the range of rooms being displayed
  room_range_start = (rooms.number - 1) * rooms_per_page + 1
  room_range_end = room_range_start + rooms_per_page - 1
  context = {
    'rooms':rooms,
    'room_range_start': room_range_start,
    'room_range_end': room_range_end,
    'total_room': all_rooms.count(),
  }
  return render(request, "admin/messages.html", context)
@login_required(login_url="/login/")
def faq_page(request):
  all_faqs = FAQ.objects.all()
  faqs_per_page = 10
  page = request.GET.get('page', 1)
  paginator = Paginator(all_faqs, faqs_per_page)
  try:
      faqs = paginator.page(page)
  except PageNotAnInteger:
     faqs = paginator.page(1)
  except EmptyPage:
        faqs = paginator.page(paginator.num_pages)

  faq_range_start = (faqs.number - 1) * faqs_per_page + 1
  faq_range_end = faq_range_start + faqs_per_page - 1
  context = {
    'faqs':faqs,
    'faq_range_start': faq_range_start,
    'faq_range_end': faq_range_end,
    'total_faqs': all_faqs.count(),
  }
  return render(request, "admin/faqs.html", context)

def chat_room_reply(request, room_uid):
    room = get_object_or_404(Room, uid=room_uid)
    messages = Message.objects.filter(room=room)
    return render(request, 'admin/reply_message.html', {'room': room, 'messages': messages})

def add_faq(request):
    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        check_if_exist = FAQ.objects.filter(question=question, answer=answer).exists()

        if check_if_exist:
            return HttpResponse('<div class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-100 dark:bg-gray-800 text-xs text-red-600 dark:text-red-400" role="alert">This question and answer already exist.</div>')
        else:
            new_faq = FAQ(question=question, answer=answer)
            new_faq.save()
            return HttpResponse('<div class="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-100 dark:bg-gray-800 text-xs text-green-600 dark:text-green-400" role="alert">Question Added Successfully</div>')
    return render(request, "admin/add_faq.html")
def update_faq(request,  qid):
    faq = get_object_or_404(FAQ, qid=qid)
    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer")


        faq.question=question
        faq.answer=answer
        faq.save()
        return HttpResponse('<div class="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-100 dark:bg-gray-800 text-xs text-green-600 dark:text-green-400" role="alert">Question Updated Successfully</div>')
    context = {
        "faq":faq
    }
    return render(request, "admin/edit_faq.html", context)

def generate_random_password():
    chars = string.ascii_uppercase + string.digits
    return 'PSWD'+''.join(random.choice(chars) for _ in range(10))
@login_required(login_url="/login/")
def add_support_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        password = generate_random_password()
        if profile_pic:
            profile_pic = profile_pic
        else:
            profile_pic = random.choice(['/user_profile_pics/1.jpg', '/user_profile_pics/2.jpg', '/user_profile_pics/3.jpg', '/user_profile_pics/4.jpg', '/user_profile_pics/5.jpg', '/user_profile_pics/6.jpg', '/user_profile_pics/7.jpg', '/user_profile_pics/8.jpg', '/user_profile_pics/9.jpg', '/user_profile_pics/10.jpg', '/user_profile_pics/11.jpg', '/user_profile_pics/12.jpg'])
        user_check_username = User.objects.filter(username=username).exists()
        user_check_mail = User.objects.filter(email=email).exists()
        if user_check_username:
            return HttpResponse('<div class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-100 dark:bg-gray-800 text-xs text-red-600 dark:text-red-400" role="alert">Username already exist.</div>')
        elif user_check_mail:
            return HttpResponse('<div class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-100 dark:bg-gray-800 text-xs text-red-600 dark:text-red-400" role="alert">This Email already exist.</div>')
        elif user_check_username and user_check_mail:
            return HttpResponse('<div class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-100 dark:bg-gray-800 text-xs text-red-600 dark:text-red-400" role="alert">Username and Email already exist.</div>')
        else:
            new_user = User(username=username, email=email, password=password)
            new_user.save()
            new_profile = Profile(user=new_user, name=name, profile_pic=profile_pic, status="Offline")
            new_profile.save()
            return HttpResponse("<div class='p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-100 dark:bg-gray-800 text-xs text-green-600 dark:text-green-400' role='alert'>{{new_profile.name}} Created Successfully <br> <span class='px-2 py-1 font-semibold leading-tight text-green-700 dark:text-green-100'>Username: {{username}} Password: {{password}} </span></div>")
    return render(request, "admin/add_support_user.html")
@login_required(login_url="/login/")
def update_support_user(request, unique_id):
    user = get_object_or_404(Profile, unique_id=unique_id)
    status = Profile.STATUS_CHOICES
    if request.method == "POST":
        name = request.POST.get('name')
        profile_pic = request.FILES.get('profile_pic')
        status = request.POST.get('status')
        if profile_pic:
            profile_pic = profile_pic
        else:
            profile_pic = user.profile_pic
        user.name = name
        user.profile_pic = profile_pic
        user.status = status
        user.save()
        return HttpResponse("<div class='p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-100 dark:bg-gray-800 text-xs text-green-600 dark:text-green-400' role='alert'>Updated Successfully <br> </div>")
    context = {
        'user':user,
        'status':status
    }
    return render(request, "admin/update_support_user.html", context)
@login_required(login_url="/login/")
def support_team_list(request):
    all_users = Profile.objects.all()
    users_per_page = 10
    page = request.GET.get('page', 1)
    paginator = Paginator(all_users, users_per_page)
    try:
      users = paginator.page(page)
    except PageNotAnInteger:
     users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    user_range_start = (users.number - 1) * users_per_page + 1
    user_range_end = user_range_start + users_per_page - 1
    context = {
        'all_users':all_users,
        'user_range_start': user_range_start,
        'user_range_end': user_range_end,
        'total_users': all_users.count(),
    }
    return render(request, "admin/support_list.html", context)