from django.urls import path
from . import views

app_name = "journal"
urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("entry/<int:entry_id>/", views.entry_detail, name="entry_detail"),
    path("api/analyze/", views.analyze_sentiment_api, name="analyze_sentiment"),
]
