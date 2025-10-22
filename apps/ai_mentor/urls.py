from django.urls import path
from . import views

app_name = 'ai_mentor'

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('session/<uuid:session_id>/', views.session_detail, name='session_detail'),
    path('send/', views.send_message, name='send_message'),
    path('new/', views.new_session, name='new_session'),
    path('my-sessions/', views.my_sessions, name='my_sessions'),
]
