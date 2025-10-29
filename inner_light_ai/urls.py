from django.contrib import admin
from django.urls import path, include
from inner_light_ai import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas principales (home y auth)
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # App del proyecto
    path('journal/', include('journal.urls')),
]

# Servir archivos de MEDIA en desarrollo (para ImageField de la comunidad)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
