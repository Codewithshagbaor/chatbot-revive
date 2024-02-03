from django.urls import path
from . import views
from . import admin_view
urlpatterns = [
    path('', views.index, name="index"),
    path('start_chat/', views.initate_chat, name="initate_chat"),
    path('dashboard/', admin_view.dashboard, name="admin_dashboard"),
    path('dashboard/messages/', admin_view.messages, name="admin_messages"),
    path('<str:room_uid>/', views.chat_room, name='chat_room'),
    # path('<str:room_uid>/post_message/', views.post_message, name='post_message'),
    # path('<str:room_uid>/get_messages/', views.get_messages, name='get_messages'),
]
