import os
import json
from django.conf import settings

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


def _client():
    if OpenAI is None:
        raise RuntimeError("Instala el SDK oficial: pip install openai>=1.0.0")
    api_key = os.environ.get('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurada. Exporta la variable o configúrala en settings.")
    org = getattr(settings, 'OPENAI_ORG', None) or os.environ.get('OPENAI_ORG')
    if org:
        return OpenAI(api_key=api_key, organization=org)
    return OpenAI(api_key=api_key)


def _sanitize(obj):
    """Elimina claves que inicien por '_' en todo el árbol."""
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items() if not str(k).startswith('_')}
    if isinstance(obj, list):
        return [_sanitize(x) for x in obj]
    return obj


def analyze_texts(entries_text, model=None):
    """
    Envía entradas del diario a OpenAI y retorna un dict seguro:
    { emociones:[], disparadores:[], recomendaciones:[], warning:?, error:? }
    """
    model = model or getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini')

    prompt = (
        "Eres un analista de hábitos y emociones. Lee estas entradas de diario (español), "
        "extrae patrones inconscientes, disparadores, emociones frecuentes, y sugiere prácticas concretas.\n"
        "Devuelve SOLO JSON válido con esta forma:\n"
        "{\n"
        '  "emociones": [{"nombre": "...", "frecuencia": 0-1, "evidencia": "..." }],\n'
        '  "disparadores": [{"nombre": "...", "evidencia": "..."}],\n'
        '  "recomendaciones": [{"practica": "...", "frecuencia": "diaria/semanal", "pasos": ["...", "..."]}]\n'
        "}\n"
        "Entradas:\n"
    )
    for i, t in enumerate(entries_text, 1):
        prompt += f"\n[{i}] {t.strip()}"

    try:
        client = _client()
        resp = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": "Responde solo con JSON válido y conciso."},
                {"role": "user", "content": prompt},
            ],
        )
        content = resp.choices[0].message.content.strip()
        data = json.loads(content)  # puede lanzar excepción -> except
        return _sanitize(data)
    except Exception as e:
        return {
            "emociones": [],
            "disparadores": [],
            "recomendaciones": [],
            "warning": None,
            "error": f"Fallo al analizar: {e}",
        }
