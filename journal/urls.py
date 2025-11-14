from django.urls import path
from . import views

app_name = "journal"

urlpatterns = [
    path("", views.journal_list, name="list"),

    # Diario / IA
    path("analyze/", views.analyze_patterns, name="analyze"),
    path("entry/<int:entry_id>/edit/", views.edit_entry, name="entry_edit"),
    path("entry/<int:entry_id>/delete/", views.delete_entry, name="entry_delete"),

    # Comunidad
    path("community/", views.community_feed, name="community"),
    path("community/post/", views.create_post, name="create_post"),
    path("community/<int:post_id>/comment/", views.add_comment, name="add_comment"),

    # 👇 aquí el cambio importante
    path(
        "community/<int:post_id>/react/<str:reaction_type>/",
        views.react_to_post,
        name="react_to_post",
    ),
]
