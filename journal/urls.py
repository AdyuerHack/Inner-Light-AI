from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.journal_list, name='list'),
    path('add/', views.journal_list, name='add'),
    path('entry/', views.journal_entry, name='entry'),
    path('community/', views.community_feed, name='community'),
    path('community/post/', views.create_post, name='create_post'),
    path('community/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('community/react/<int:post_id>/<str:reaction_type>/', views.react_to_post, name='react_to_post'),
]
