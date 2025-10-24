from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# 🏠 Página principal
def home(request):
    """
    Muestra la página de bienvenida con opciones para iniciar sesión o registrarse.
    """
    return render(request, 'journal/home.html')


# 🧘 Registro de usuarios
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Registro exitoso. Inicia sesión ahora.')
        return redirect('login')

    return render(request, 'journal/home.html', {'show_register': True})


# 🔐 Inicio de sesión → redirige al diario
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username} 🌟')
            return redirect('journal:list')  # 👈 redirige al diario
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'journal/home.html', {'show_login': True})


# 🚪 Cerrar sesión
def user_logout(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('home')
