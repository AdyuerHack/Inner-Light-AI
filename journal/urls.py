from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.journal_entry, name='journal_entry'),
    path('list/', views.journal_list, name='journal_list'),
]
