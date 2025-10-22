from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("journal/", include("apps.journal.urls")),
    path("meditation/", include("apps.meditation.urls")),
    path("community/", include("apps.community.urls")),
    path("mentor/", include("apps.ai_mentor.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
