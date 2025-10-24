from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.journal_list, name='list'),
    path('add/', views.journal_list, name='add'),  # para añadir entradas al diario
    path('community/', views.community_feed, name='community'),  # muestra comunidad
    path('community/post/', views.create_post, name='create_post'),  # 👈 NUEVO
    path('community/react/<int:post_id>/<str:reaction_type>/', views.react_to_post, name='react_to_post'),  # reacciones
]
