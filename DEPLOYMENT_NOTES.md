# 🚀 Notas de Despliegue - Inner Light AI

## ✅ Checklist Pre-Despliegue

### Desarrollo Local (Completado)
- [x] Base de datos configurada (SQLite)
- [x] Migraciones aplicadas
- [x] Datos semilla cargados (8 meditaciones)
- [x] Archivos estáticos configurados
- [x] Variables de entorno en .env
- [x] Servidor de desarrollo funcional

### Producción (Pendiente)

#### Configuración Esencial
- [ ] Cambiar SECRET_KEY a valor seguro (50+ caracteres)
- [ ] Establecer DEBUG=False
- [ ] Configurar ALLOWED_HOSTS con dominio real
- [ ] Cambiar a base de datos PostgreSQL/MySQL
- [ ] Configurar archivos estáticos con WhiteNoise o S3
- [ ] Habilitar HTTPS
- [ ] Configurar variables de entorno seguras

#### Seguridad
- [ ] Activar SECURE_HSTS_SECONDS = 31536000
- [ ] Activar SECURE_SSL_REDIRECT = True
- [ ] Activar SESSION_COOKIE_SECURE = True
- [ ] Activar CSRF_COOKIE_SECURE = True
- [ ] Configurar CORS correctamente
- [ ] Implementar rate limiting
- [ ] Configurar firewall

#### Monitoreo y Logs
- [ ] Configurar Sentry para errores
- [ ] Implementar logging a archivos
- [ ] Configurar monitoreo de uptime
- [ ] Configurar alertas
- [ ] Implementar analytics (opcional)

#### Backups
- [ ] Backup automático de base de datos
- [ ] Backup de archivos subidos
- [ ] Plan de recuperación

---

## 🌐 Opciones de Hosting

### Opción 1: Heroku (Más Fácil)

**Pros:** Fácil, gratuito (tier básico), deploys automáticos  
**Contras:** Límites en tier gratuito, puede dormir apps

```bash
# 1. Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Crear app
heroku create innerlight-ai

# 4. Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini

# 5. Configurar variables
heroku config:set SECRET_KEY="tu-secret-key-seguro-aqui"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="innerlight-ai.herokuapp.com"

# 6. Deploy
git push heroku main

# 7. Migrar
heroku run python manage.py migrate
heroku run python manage_seed_data.py

# 8. Abrir
heroku open
```

**Archivos necesarios:**
- `Procfile`: `web: gunicorn innerlight.wsgi`
- `runtime.txt`: `python-3.13.0`
- Actualizar `requirements.txt` con `gunicorn`, `whitenoise`, `psycopg2`

### Opción 2: Railway (Recomendado)

**Pros:** Moderno, fácil, buen tier gratuito, PostgreSQL incluido  
**Contras:** Relativamente nuevo

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Inicializar
railway init

# 4. Agregar PostgreSQL
railway add postgresql

# 5. Deploy
railway up

# 6. Configurar variables en dashboard
# railway.app -> Settings -> Variables

# 7. Migrar
railway run python manage.py migrate
railway run python manage_seed_data.py
```

### Opción 3: Render (Alternativa)

**Pros:** Fácil, moderno, SSL gratis  
**Contras:** Menos conocido

Pasos similares a Heroku, todo desde el dashboard web.

### Opción 4: VPS (DigitalOcean, AWS, etc.)

**Pros:** Control total, escalabilidad  
**Contras:** Más complejo, requiere conocimientos DevOps

**Stack recomendado:**
- Ubuntu 22.04 LTS
- Nginx (web server)
- Gunicorn (WSGI server)
- PostgreSQL (database)
- Redis (cache - opcional)
- Supervisor (process manager)
- Let's Encrypt (SSL)

---

## 📦 Archivos para Producción

### Procfile (Heroku/Railway)
```
web: gunicorn innerlight.wsgi:application --log-file -
release: python manage.py migrate
```

### runtime.txt
```
python-3.13.0
```

### requirements.txt (Producción)
```
Django>=5.0,<6.0
django-environ>=0.11.2
djangorestframework>=3.14.0
transformers>=4.35.0
torch>=2.1.0
openai>=1.3.0
anthropic>=0.7.0
textblob>=0.17.1
python-dotenv>=1.0.0
pillow>=10.1.0
markdown>=3.5.0
bleach>=6.1.0
channels>=4.0.0
redis>=5.0.0
gunicorn>=21.2.0
whitenoise>=6.6.0
psycopg2-binary>=2.9.9
dj-database-url>=2.1.0
```

### .env.production
```env
DEBUG=False
SECRET_KEY=tu-secret-key-super-seguro-de-50-caracteres-minimo-12345678
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Opcional
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Seguridad
SECURE_HSTS_SECONDS=31536000
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🔧 Configuración de settings.py para Producción

Agregar al final de `innerlight/settings.py`:

```python
# Producción
if not DEBUG:
    # Static files
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Security
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', 31536000))
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Database - usar DATABASE_URL de entorno
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
```

---

## 📊 Monitoreo Recomendado

### Sentry (Errores)
```bash
pip install sentry-sdk
```

En settings.py:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn="tu-sentry-dsn",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
```

### Uptime Monitoring
- UptimeRobot (gratis)
- Pingdom
- StatusCake

### Analytics (Opcional)
- Google Analytics
- Plausible (privacy-focused)
- Simple Analytics

---

## 🗄️ PostgreSQL en Producción

### Configuración recomendada

```sql
-- Crear usuario
CREATE USER innerlight WITH PASSWORD 'password-seguro';

-- Crear base de datos
CREATE DATABASE innerlight OWNER innerlight;

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE innerlight TO innerlight;

-- Configurar para Django
ALTER ROLE innerlight SET client_encoding TO 'utf8';
ALTER ROLE innerlight SET default_transaction_isolation TO 'read committed';
ALTER ROLE innerlight SET timezone TO 'UTC';
```

### Backups automáticos

Heroku/Railway lo hacen automáticamente.

Para VPS:
```bash
# Crear script de backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump innerlight > /backups/innerlight_$DATE.sql
# Mantener solo últimos 30 días
find /backups -name "innerlight_*.sql" -mtime +30 -delete
```

Agregar a crontab:
```bash
0 2 * * * /usr/local/bin/backup_db.sh
```

---

## 🔐 Generar SECRET_KEY Seguro

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

O en bash:
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 📈 Optimización de Rendimiento

### Caché con Redis

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session en Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### Comprimir Respuestas

```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... resto
]
```

### CDN para Estáticos

Usar Cloudflare, AWS CloudFront, o similar.

---

## 🧪 Testing Pre-Deploy

```bash
# 1. Verificar en modo producción local
DEBUG=False python manage.py check --deploy

# 2. Ejecutar tests
python manage.py test

# 3. Verificar estáticos
python manage.py collectstatic --noinput

# 4. Probar con Gunicorn
gunicorn innerlight.wsgi:application --bind 0.0.0.0:8000

# 5. Probar migraciones
python manage.py migrate --check

# 6. Verificar seguridad
python manage.py check --deploy
```

---

## 📞 Soporte Post-Deploy

### Logs importantes
```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# VPS
tail -f /var/log/nginx/error.log
tail -f /var/log/supervisor/innerlight.log
```

### Comandos útiles
```bash
# Heroku
heroku run python manage.py shell
heroku run python manage.py dbshell
heroku restart

# Railway
railway run python manage.py shell
railway restart
```

---

## 🎯 Checklist Final

Antes de considerar el deploy completo:

- [ ] App accesible vía URL pública
- [ ] HTTPS funcionando
- [ ] Base de datos funcionando
- [ ] Archivos estáticos sirven correctamente
- [ ] Formularios funcionan (POST)
- [ ] Login/registro funciona
- [ ] Todas las páginas cargan
- [ ] No hay errores en logs
- [ ] Backups configurados
- [ ] Monitoreo activo
- [ ] DNS configurado correctamente

---

## 📚 Recursos Adicionales

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Heroku Django Tutorial](https://devcenter.heroku.com/articles/django-app-configuration)
- [Railway Documentation](https://docs.railway.app/)
- [DigitalOcean Django Deployment](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn)

---

**Estado Actual:** ✅ Listo para desarrollo local  
**Próximo Paso:** Elegir plataforma de hosting y desplegar  

*Última actualización: 2025-10-22*
