from django.urls import path
from . import views

app_name = "journal"
urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("meditaciones/", views.meditations, name="meditations"),
    path("comunidad/", views.community, name="community"),
    path("chat/", views.chat, name="chat"),
]
