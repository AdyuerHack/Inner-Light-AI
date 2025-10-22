from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_home, name='home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),
    path('post/<uuid:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<uuid:post_id>/like/', views.toggle_like, name='toggle_like'),
]
