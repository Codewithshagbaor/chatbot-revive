# views.py
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

def index(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        
        greetings = ['hello', 'hi']
        no_list = ['no']
        my_list = [
            "if you have any more questions for me today. If not, feel free to let me know if you have any questions in the future.",
            "I hope you're enjoying your time with me. Do you have any more questions or would you like to chat again in the future?",
            "if you had any further questions or needed assistance with anything else. Let me know if you do!",
            "I'm here to help. Do you have any other questions or would you like to ask something else later?",
            "I'm always here to help. Do you have any more questions or need assistance with anything else? Let me know if you do!",
        ]
        question = random.choice(my_list)

        if any(word in user_message.lower().split() for word in greetings):
            response = "How can I help you?"
            faq_options = FAQ.objects.values_list('question', flat=True)
            return JsonResponse({'response': response, 'faq_options': list(faq_options)})

        if any(word in user_message.lower() for word in ['yes']):
            response = "How can I help you?"
            faq_options = FAQ.objects.values_list('question', flat=True)
            return JsonResponse({'response': response, 'faq_options': list(faq_options)})
        if any(word in user_message.lower().split() for word in no_list):
            response = "Okay Have a nice day"
            return JsonResponse({'response': response})

        # Check if the user's message is a question in the database
        faq = FAQ.objects.filter(question__iexact=user_message).first()

        if faq:
            response = faq.answer + question
        else:
            response = "I'm sorry, I don't understand that question."

        return JsonResponse({'response': response})

    return render(request, 'chat_home.html')

def chat_room(request, room_uid):
    room = get_object_or_404(Room, uid=room_uid)
    messages = Message.objects.filter(room=room)
    return render(request, 'chat_room.html', {'room': room, 'messages': messages})

# def post_message(request, room_uid):
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         room = Room.objects.get(uid=room_uid)
#         Message.objects.create(room=room, content=content)
#     return redirect('chat_room', room_uid=room_uid)


# def get_messages(request, room_uid):
#     room = Room.objects.get(uid=room_uid)
#     messages = list(Message.objects.filter(room=room).values())
#     return JsonResponse({'messages': messages})

def initate_chat(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        uid = 'UID' + ''.join(random.choice(string.digits) for _ in range(10))


        new_room = Room.objects.create(
            title=content,
            user_name=user_name,
            user_email=user_email,
            uid=uid,
        )
        new_room.save()
        room_message = Message.objects.create(
            username=user_name,
            room = new_room,
            content=content,
        )
        room_message.save()
        return redirect('chat_room', new_room.uid)
    return render(request, "chat/chat_with_intitate.html")