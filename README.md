# 🌟 Inner Light AI – Mentor Espiritual & Emocional 24/7  

**Inner Light AI** es un prototipo de aplicación web con inteligencia artificial que funciona como un **mentor personal 24/7**, acompañando a los usuarios en su crecimiento emocional y espiritual.  

El proyecto está diseñado para un **contexto académico**, priorizando funcionalidades esenciales (MVP) bajo la metodología **MoSCoW**.  

---

## 🎯 Objetivos del Proyecto  

- Ofrecer un **mentor IA disponible 24/7** para acompañamiento espiritual y emocional.  
- Detectar **patrones emocionales** a través de un diario inteligente.  
- Brindar **meditaciones guiadas simples** adaptadas al estado emocional.  
- Fomentar hábitos de bienestar con **recordatorios personalizados**.  
- Crear una **comunidad anónima segura** donde los usuarios compartan reflexiones.  
- Garantizar la **seguridad y el anonimato** de la información del usuario.  

---

## ✨ Características Implementadas (MVP)

### 🟥 Must Have (Completado)
- ✅ **FR1: Diario Emocional** - Sistema completo de diario con interfaz moderna
- ✅ **FR2: Análisis de Sentimientos** - Análisis automático con TextBlob y detección de emociones
- ✅ **FR3: Meditaciones Guiadas** - 8 meditaciones predefinidas adaptadas a diferentes estados emocionales
- ✅ **FR5: Comunidad Anónima** - Sistema de publicaciones y comentarios con perfiles anónimos
- ✅ **FR10: Chat Mentor IA 24/7** - Chat inteligente con respuestas predefinidas y soporte para OpenAI/Anthropic
- ✅ **NFR1: Seguridad de Datos** - Configuración de seguridad Django con CSRF, cookies seguras
- ✅ **NFR7: Anonimato Garantizado** - Perfiles anónimos con nombres y colores generados automáticamente

---

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.13+ 
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio o descomprimir el proyecto**
   ```bash
   cd /ruta/al/proyecto
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Edita .env si necesitas cambiar configuraciones
   ```

4. **Configurar base de datos**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. **Poblar con datos iniciales** (Meditaciones)
   ```bash
   python3 manage_seed_data.py
   ```

6. **Crear superusuario** (opcional, para panel de admin)
   ```bash
   python3 manage.py createsuperuser
   ```

7. **Ejecutar el servidor de desarrollo**
   ```bash
   python3 manage.py runserver
   ```

8. **Acceder a la aplicación**
   - Aplicación principal: http://127.0.0.1:8000/
   - Panel de administración: http://127.0.0.1:8000/admin/

---

## 📁 Estructura del Proyecto

```
innerlight/
├── apps/
│   ├── journal/          # Diario emocional
│   │   ├── models.py     # Modelo JournalEntry
│   │   ├── views.py      # Vistas y API
│   │   └── sentiment_analysis.py  # Servicio de análisis
│   ├── meditation/       # Meditaciones guiadas
│   │   ├── models.py     # Meditation, MeditationSession
│   │   └── views.py      # Vistas de meditaciones
│   ├── community/        # Comunidad anónima
│   │   ├── models.py     # Posts, Comments, Likes
│   │   └── views.py      # Vistas de comunidad
│   └── ai_mentor/        # Chat con mentor IA
│       ├── models.py     # ChatSession, ChatMessage
│       ├── views.py      # Vistas de chat
│       └── ai_service.py # Servicio de IA
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base con Tailwind CSS
│   ├── index.html        # Página principal
│   ├── journal/
│   ├── meditation/
│   ├── community/
│   └── ai_mentor/
├── innerlight/           # Configuración Django
│   ├── settings.py       # Configuración principal
│   └── urls.py           # URLs principales
├── static/               # Archivos estáticos
├── manage.py             # Script de gestión Django
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

---

## 🎨 Tecnologías Utilizadas

### Backend
- **Django 5.0** - Framework web principal
- **Python 3.13** - Lenguaje de programación
- **SQLite** - Base de datos (fácilmente reemplazable por PostgreSQL)

### Frontend
- **Tailwind CSS 3** - Framework CSS moderno
- **Font Awesome 6** - Íconos
- **Vanilla JavaScript** - Interacciones dinámicas

### Inteligencia Artificial
- **TextBlob** - Análisis de sentimientos básico
- **OpenAI GPT-3.5** (opcional) - Chat avanzado
- **Anthropic Claude** (opcional) - Chat avanzado alternativo

---

## 🔧 Configuración Avanzada

### Integración con OpenAI o Anthropic

Para habilitar respuestas IA avanzadas en el mentor:

1. Obtén una API key de [OpenAI](https://platform.openai.com/) o [Anthropic](https://www.anthropic.com/)

2. Agrega tu API key al archivo `.env`:
   ```bash
   OPENAI_API_KEY=tu-api-key-aqui
   # O
   ANTHROPIC_API_KEY=tu-api-key-aqui
   ```

3. El sistema detectará automáticamente la API key y usará el servicio correspondiente.

**Nota:** Sin API key, el mentor IA funciona con respuestas predefinidas inteligentes basadas en palabras clave.

---

## 📊 Características Detalladas

### 📖 Diario Emocional
- Entradas ilimitadas con timestamps
- Análisis automático de sentimientos (positivo/negativo/neutral)
- Detección de emociones específicas (alegría, tristeza, ansiedad, etc.)
- Visualización del tono emocional
- Análisis en tiempo real mientras escribes
- Soporte para usuarios anónimos

### 🧘 Meditaciones Guiadas
- 8 meditaciones predefinidas
- Clasificadas por emoción objetivo:
  - Calma
  - Ansiedad
  - Tristeza
  - Enojo
  - Alegría
  - Estrés
  - Neutral
- Temporizador integrado
- Registro de sesiones completadas
- Evaluación emocional antes/después

### 👥 Comunidad Anónima
- Perfiles anónimos con nombres únicos generados
- Colores de avatar personalizados
- 6 categorías de publicaciones:
  - Reflexión
  - Gratitud
  - Desafío
  - Victoria
  - Pregunta
  - Apoyo
- Sistema de likes
- Comentarios anónimos
- Moderación automática básica (detección de contenido sensible)

### 💬 Mentor IA 24/7
- Chat conversacional inteligente
- Historial de sesiones
- Respuestas empáticas y reflexivas
- Integración con análisis de sentimientos del diario
- Contexto emocional del usuario
- Respuestas predefinidas inteligentes (sin API)
- Soporte opcional para OpenAI/Anthropic

---

## 🔒 Seguridad y Privacidad

- ✅ Protección CSRF en todos los formularios
- ✅ Cookies HTTP-only y seguras
- ✅ Anonimato total en la comunidad
- ✅ Datos de chat cifrados en sesión
- ✅ Opción de uso sin registro
- ✅ Sin tracking de terceros
- ✅ Sin analytics invasivos

---

## 📊 MoSCoW Prioritization  

### Tabla Implementada

| 🟥 Must Have (M) | Estado | 🟨 Should Have (S) | Estado |
|------------------|--------|-------------------|---------|
| FR1: Diario emocional | ✅ Completado | FR4: Recordatorios | ⏸️ Futuro |
| FR2: Análisis de sentimientos | ✅ Completado | FR6: Mentores pares | ⏸️ Futuro |
| FR3: Meditaciones guiadas | ✅ Completado | NFR2: Disponibilidad | ✅ Completado |
| FR5: Comunidad anónima | ✅ Completado | NFR5: Usabilidad | ✅ Completado |
| FR10: Chat IA 24/7 | ✅ Completado | | |
| NFR1: Seguridad | ✅ Completado | | |
| NFR7: Anonimato | ✅ Completado | | |

---

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Error: "STATICFILES_DIRS does not exist"
```bash
mkdir -p static
```

### Error al ejecutar migraciones
```bash
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
```

### Puerto 8000 ya en uso
```bash
python3 manage.py runserver 8001
```

---

## 🚀 Despliegue en Producción

### Configuraciones Importantes

1. **Cambiar SECRET_KEY** en `.env`
2. **Configurar DEBUG=False**
3. **Actualizar ALLOWED_HOSTS** con tu dominio
4. **Usar PostgreSQL o MySQL** en lugar de SQLite
5. **Configurar servidor web** (Nginx + Gunicorn)
6. **Habilitar HTTPS**
7. **Configurar copias de seguridad** de la base de datos

### Ejemplo con Gunicorn
```bash
pip install gunicorn
gunicorn innerlight.wsgi:application --bind 0.0.0.0:8000
```

---

## 🧪 Testing

```bash
# Ejecutar tests
python3 manage.py test

# Crear datos de prueba
python3 manage_seed_data.py

# Verificar configuración
python3 manage.py check
```

---

## 📖 API Endpoints

### Journal (Diario)
- `GET /journal/` - Lista de entradas
- `POST /journal/create/` - Crear entrada
- `POST /journal/api/analyze/` - Analizar sentimiento (AJAX)

### Meditation (Meditaciones)
- `GET /meditation/` - Lista de meditaciones
- `GET /meditation/<id>/` - Detalle de meditación
- `POST /meditation/<id>/start/` - Iniciar sesión

### Community (Comunidad)
- `GET /community/` - Feed de publicaciones
- `POST /community/post/create/` - Crear publicación
- `POST /community/post/<id>/like/` - Toggle like

### AI Mentor
- `GET /mentor/` - Página de chat
- `POST /mentor/send/` - Enviar mensaje
- `POST /mentor/new/` - Nueva sesión

---

## 🤝 Contribuciones

Este es un proyecto académico, pero las sugerencias son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto es de código abierto para fines académicos y educativos.

---

## 👨‍💻 Autor  

**Adyuer de Jesús Ojeda Badel**  
- Proyecto académico – Ingeniería de Sistemas  
- Universidad EAFIT – 2025  

---

## 🙏 Agradecimientos

- Universidad EAFIT por el apoyo académico
- Comunidad de Django por la excelente documentación
- Todos los que buscan crecimiento personal y espiritual

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Consulta la [documentación de Django](https://docs.djangoproject.com/)
3. Contacta al autor a través de la universidad

---

## 🌟 Roadmap Futuro

- [ ] App móvil (React Native / Flutter)
- [ ] Integración con wearables
- [ ] Sistema de gamificación
- [ ] Análisis de voz en tiempo real
- [ ] Recomendaciones personalizadas con ML
- [ ] Exportación de datos (PDF, CSV)
- [ ] Modo offline
- [ ] Temas personalizables
- [ ] Multiidioma

---

**¡Gracias por usar Inner Light AI! 🌟💫**

*"La luz más brillante está dentro de ti"*
