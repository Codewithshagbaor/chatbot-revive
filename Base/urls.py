from django.urls import path
from . import views
from . import admin_view
urlpatterns = [
    path('', views.index, name="index"),
    path('start_chat/', views.initate_chat, name="initate_chat"),
    path('dashboard/', admin_view.dashboard, name="admin_dashboard"),
    path('dashboard/messages/', admin_view.messages, name="admin_messages"),
    path('dashboard/support_list/', admin_view.support_team_list, name="user_list"),
    path('dashboard/add_user/', admin_view.add_support_user, name="add_support_user"),
    path('dashboard/faqs/', admin_view.faq_page, name="faq_page"),
    path('dashboard/faqs/add/', admin_view.add_faq, name="add_faq"),
    path('dashboard/faqs/<str:qid>/', admin_view.update_faq, name="update_faq"),
    path('<str:room_uid>/reply/', admin_view.chat_room_reply, name='chat_room_reply'),
    path('<str:room_uid>/', views.chat_room, name='chat_room'),
    path('dashboard/<str:unique_id>/', admin_view.update_support_user, name="update_support_user"),
    # path('<str:room_uid>/post_message/', views.post_message, name='post_message'),
    # path('<str:room_uid>/get_messages/', views.get_messages, name='get_messages'),
]
