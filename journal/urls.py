# journal/urls.py
from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    # Diario
    path('', views.journal_list, name='list'),
    path('analyze/', views.analyze_patterns, name='analyze'),

    # Comunidad (tu funcionalidad existente)
    path('community/', views.community_feed, name='community'),
    path('community/create/', views.create_post, name='create_post'),
    path('community/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('community/react/<int:post_id>/<str:reaction_type>/', views.react_to_post, name='react_to_post'),
]
