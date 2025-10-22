from django.urls import path
from . import views

app_name = 'meditation'

urlpatterns = [
    path('', views.meditation_list, name='list'),
    path('<int:meditation_id>/', views.meditation_detail, name='detail'),
    path('<int:meditation_id>/start/', views.start_session, name='start_session'),
    path('session/<int:session_id>/complete/', views.complete_session, name='complete_session'),
    path('my-sessions/', views.my_sessions, name='my_sessions'),
]
