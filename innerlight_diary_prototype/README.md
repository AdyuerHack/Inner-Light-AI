# Inner Light AI – MVP (Django)

Ejecutar localmente:

```bash
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```

Funcionalidades MVP:
- Diario emocional con análisis de sentimiento local (léxico simple en español)
- Meditaciones guiadas simples
- Comunidad anónima básica
- Chat mentor IA 24/7 (reglas simples)

Privacidad/anonimato:
- Sin PII; se usa cookie opaca `il_anon` para agrupar entradas anónimas
- Cookies `SameSite=Lax` y `Secure` en producción

Variables de entorno (opcional): copia `.env.example` a `.env`.
