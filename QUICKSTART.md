# ⚡ Inicio Rápido - Inner Light AI

## 🚀 Empezar en 5 Minutos

### Paso 1: Instalar Dependencias (2 min)
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar Base de Datos (1 min)
```bash
python3 manage.py migrate
python3 manage_seed_data.py
```

### Paso 3: Ejecutar el Servidor (30 seg)
```bash
python3 manage.py runserver
```

### Paso 4: Abrir en el Navegador (30 seg)
```
http://127.0.0.1:8000/
```

---

## 🎉 ¡Listo!

Ya puedes:
- ✅ Escribir en tu diario emocional
- ✅ Ver análisis de sentimientos en tiempo real
- ✅ Probar las 8 meditaciones guiadas
- ✅ Compartir en la comunidad anónima
- ✅ Chatear con el mentor IA

---

## 🔐 (Opcional) Crear Cuenta de Admin

Para acceder al panel de administración:

```bash
python3 manage.py createsuperuser
```

Luego visita: http://127.0.0.1:8000/admin/

---

## 📱 Probar las Funcionalidades

### 1. Diario Emocional
- Ve a "Diario" en el menú
- Escribe cómo te sientes hoy
- Observa el análisis de sentimientos automático
- Mira tus entradas guardadas

### 2. Meditaciones
- Ve a "Meditaciones"
- Filtra por tu emoción actual
- Inicia una meditación guiada
- Completa la sesión y registra tu experiencia

### 3. Comunidad Anónima
- Ve a "Comunidad"
- Lee las publicaciones de otros (si hay)
- Comparte tu propia reflexión (100% anónimo)
- Dale like y comenta en otras publicaciones

### 4. Mentor IA
- Ve a "Mentor IA"
- Escribe un mensaje al mentor
- Recibe una respuesta empática
- Continúa la conversación

---

## 🆘 Problemas?

### Error de instalación de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Puerto 8000 ocupado
```bash
python3 manage.py runserver 8001
```

### Base de datos corrupta
```bash
rm db.sqlite3
python3 manage.py migrate
python3 manage_seed_data.py
```

---

## 🎯 Siguiente Nivel

Para configuración avanzada, ver:
- `INSTALL.md` - Guía completa de instalación
- `README.md` - Documentación completa
- `FEATURES.md` - Lista de todas las características

---

## 💡 Tips

1. **Usa el modo anónimo:** No necesitas registrarte para probar la app
2. **Prueba el análisis en tiempo real:** Escribe más de 50 caracteres en el diario
3. **Explora todas las meditaciones:** Hay 8 diferentes para distintas emociones
4. **Activa la API de IA:** Agrega tu OPENAI_API_KEY en .env para respuestas avanzadas

---

**¡Disfruta de Inner Light AI! 🌟**
