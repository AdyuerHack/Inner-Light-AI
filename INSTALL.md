# 📦 Guía de Instalación Detallada - Inner Light AI

Esta guía te llevará paso a paso para instalar y ejecutar Inner Light AI en tu máquina local.

---

## 📋 Requisitos del Sistema

### Mínimos
- **Sistema Operativo:** Windows 10+, macOS 10.14+, o Linux (Ubuntu 20.04+)
- **RAM:** 2 GB mínimo
- **Espacio en Disco:** 500 MB
- **Python:** 3.13 o superior
- **Navegador:** Chrome, Firefox, Safari o Edge (versión reciente)

### Recomendados
- **RAM:** 4 GB o más
- **Espacio en Disco:** 1 GB
- **Conexión a Internet:** Para descargar dependencias

---

## 🔧 Instalación de Prerequisitos

### 1. Instalar Python

#### Windows
1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marca "Add Python to PATH"
3. Verifica la instalación:
   ```cmd
   python --version
   ```

#### macOS
```bash
brew install python@3.13
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.13 python3-pip
```

### 2. Verificar pip
```bash
pip --version
```

Si pip no está instalado:
```bash
python -m ensurepip --upgrade
```

---

## 📥 Instalación de Inner Light AI

### Opción A: Desde el repositorio

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd innerlight

# 2. Crear entorno virtual (recomendado)
python3 -m venv venv

# 3. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Copiar archivo de configuración
cp .env.example .env

# 6. Configurar base de datos
python3 manage.py migrate

# 7. Poblar con datos iniciales
python3 manage_seed_data.py

# 8. (Opcional) Crear superusuario
python3 manage.py createsuperuser

# 9. Ejecutar servidor
python3 manage.py runserver
```

### Opción B: Desde archivo ZIP

```bash
# 1. Descomprimir el archivo
unzip innerlight.zip
cd innerlight

# 2. Seguir pasos 2-9 de la Opción A
```

---

## ⚙️ Configuración Avanzada

### Base de Datos PostgreSQL (Producción)

1. Instalar PostgreSQL:
   ```bash
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   ```

2. Crear base de datos:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE innerlight;
   CREATE USER innerlight_user WITH PASSWORD 'tu_password_seguro';
   GRANT ALL PRIVILEGES ON DATABASE innerlight TO innerlight_user;
   \q
   ```

3. Instalar adaptador:
   ```bash
   pip install psycopg2-binary
   ```

4. Actualizar `.env`:
   ```env
   DATABASE_URL=postgresql://innerlight_user:tu_password_seguro@localhost:5432/innerlight
   ```

5. Migrar:
   ```bash
   python3 manage.py migrate
   ```

### Configurar API de IA (Opcional)

#### OpenAI

1. Obtener API key en https://platform.openai.com/
2. Agregar a `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   ```

#### Anthropic Claude

1. Obtener API key en https://www.anthropic.com/
2. Agregar a `.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   ```

---

## 🧪 Verificación de Instalación

### 1. Verificar que el servidor funciona

```bash
python3 manage.py runserver
```

Deberías ver:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 2. Verificar que las páginas cargan

Abre en tu navegador:
- http://127.0.0.1:8000/ (Página principal)
- http://127.0.0.1:8000/journal/ (Diario)
- http://127.0.0.1:8000/meditation/ (Meditaciones)
- http://127.0.0.1:8000/community/ (Comunidad)
- http://127.0.0.1:8000/mentor/ (Mentor IA)

### 3. Verificar base de datos

```bash
python3 manage.py shell
```

En el shell de Python:
```python
from apps.meditation.models import Meditation
print(Meditation.objects.count())  # Debería mostrar 8
```

---

## 🔄 Actualización

Para actualizar a una nueva versión:

```bash
# 1. Actualizar código
git pull origin main
# o descomprimir nueva versión

# 2. Actualizar dependencias
pip install -r requirements.txt --upgrade

# 3. Aplicar nuevas migraciones
python3 manage.py migrate

# 4. Actualizar datos iniciales
python3 manage_seed_data.py

# 5. Recolectar archivos estáticos (producción)
python3 manage.py collectstatic --noinput
```

---

## 🐛 Solución de Problemas Comunes

### Error: "Port 8000 is already in use"

**Solución:**
```bash
# Usar otro puerto
python3 manage.py runserver 8001

# O encontrar y matar el proceso
# Linux/macOS:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "ModuleNotFoundError: No module named 'django'"

**Solución:**
```bash
# Verificar que el entorno virtual está activado
# Si no, activarlo y reinstalar
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### Error: "OperationalError: no such table"

**Solución:**
```bash
python3 manage.py migrate --run-syncdb
```

### Error: "ImproperlyConfigured: SECRET_KEY"

**Solución:**
```bash
# Asegurarse de que existe .env
cp .env.example .env
# O establecer variable de entorno
export SECRET_KEY="tu-secret-key-aqui"
```

### Problemas con TextBlob

**Solución:**
```bash
python3 -m textblob.download_corpora
```

### Problemas con torch en macOS M1/M2

**Solución:**
```bash
pip uninstall torch
pip install torch --no-cache-dir
```

---

## 🚀 Optimización de Rendimiento

### 1. Caché de Redis (Opcional)

```bash
# Instalar Redis
# Ubuntu/Debian:
sudo apt install redis-server

# macOS:
brew install redis

# Instalar cliente Python
pip install redis django-redis

# Actualizar settings.py (ya configurado)
```

### 2. Comprimir archivos estáticos

```bash
pip install django-compressor
python3 manage.py compress
```

### 3. Habilitar modo debug toolbar (desarrollo)

```bash
pip install django-debug-toolbar
# Agregar a INSTALLED_APPS en settings.py
```

---

## 📊 Monitoreo

### Ver logs

```bash
# Logs de Django
python3 manage.py runserver --verbosity 2

# Logs de errores
tail -f /var/log/innerlight/error.log
```

### Estadísticas de la base de datos

```bash
python3 manage.py shell
```

```python
from apps.journal.models import JournalEntry
from apps.meditation.models import Meditation, MeditationSession
from apps.community.models import CommunityPost

print(f"Entradas de diario: {JournalEntry.objects.count()}")
print(f"Meditaciones: {Meditation.objects.count()}")
print(f"Sesiones completadas: {MeditationSession.objects.filter(completed=True).count()}")
print(f"Posts en comunidad: {CommunityPost.objects.count()}")
```

---

## 🔐 Seguridad en Producción

### Lista de verificación

- [ ] Cambiar `SECRET_KEY` en `.env`
- [ ] Configurar `DEBUG=False`
- [ ] Actualizar `ALLOWED_HOSTS`
- [ ] Usar HTTPS
- [ ] Configurar firewall
- [ ] Habilitar CSRF protection
- [ ] Configurar CORS adecuadamente
- [ ] Backups automáticos de BD
- [ ] Monitoreo de errores (Sentry)
- [ ] Rate limiting en APIs
- [ ] Actualizar dependencias regularmente

---

## 📚 Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Tutorial de Python](https://docs.python.org/3/tutorial/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Font Awesome Icons](https://fontawesome.com/icons)

---

## 💬 Soporte

Si tienes problemas durante la instalación:

1. **Revisa esta guía completa**
2. **Consulta la documentación oficial de Django**
3. **Busca el error en Google/Stack Overflow**
4. **Contacta al equipo de desarrollo**

---

**¡Feliz instalación! 🎉**
