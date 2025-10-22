from __future__ import annotations

import re
import secrets
from dataclasses import dataclass
from typing import Tuple

from django.conf import settings


COOKIE_NAME = "il_anon"


def _token() -> str:
    return secrets.token_hex(16)


def ensure_anon_cookie(request, response) -> str:
    """Return anon_id and ensure cookie is set on the response.

    - If cookie is present, returns it as-is.
    - If missing, generates a new opaque token and sets an HTTPOnly cookie.
    """
    anon_id = request.COOKIES.get(COOKIE_NAME)
    if not anon_id:
        anon_id = _token()
        response.set_cookie(
            COOKIE_NAME,
            anon_id,
            max_age=60 * 60 * 24 * 365 * 3,  # 3 años
            httponly=True,
            samesite="Lax",
            secure=not bool(getattr(settings, "DEBUG", True)),
        )
    return anon_id


@dataclass
class Sentiment:
    label: str  # "positivo" | "negativo" | "neutral"
    score: float  # [-1.0, 1.0]
    tone: str


_POS_WORDS = {
    "gracias",
    "agradecido",
    "feliz",
    "contento",
    "alegre",
    "paz",
    "calma",
    "sereno",
    "esperanza",
    "amor",
    "bien",
    "tranquilo",
    "bendecido",
}

_NEG_WORDS = {
    "triste",
    "ansioso",
    "miedo",
    "enojo",
    "enojado",
    "ira",
    "estres",
    "estrés",
    "cansado",
    "agotado",
    "solo",
    "soledad",
    "culpa",
    "vergüenza",
    "verguenza",
    "preocupado",
    "dolor",
    "depresion",
    "depresión",
}

_TONE_MAP = [
    (re.compile(r"\bgracias|agradecid[ao]|bendecid[ao]\b", re.I), "agradecido"),
    (re.compile(r"\bfeliz|alegr[ea]|content[oa]\b", re.I), "alegre"),
    (re.compile(r"\bansios[oa]|preocupad[oa]|estr[eé]s\b", re.I), "ansioso"),
    (re.compile(r"\btrist[ea]|depresi[oó]n\b", re.I), "triste"),
    (re.compile(r"\bpaz|calma|seren[oa]|tranquil[oa]\b", re.I), "en paz"),
    (re.compile(r"\bira|enojo|enojad[oa]\b", re.I), "molesto"),
]


def _normalize(text: str) -> Tuple[str, list[str]]:
    lowered = text.lower()
    # quick tokenization by non-letters, keep accents simple
    tokens = re.findall(r"[\wáéíóúñü]+", lowered, flags=re.I)
    return lowered, tokens


def analyze_sentiment(text: str) -> Sentiment:
    # very small lexicon-based heuristic suitable for MVP without external services
    _, tokens = _normalize(text)
    pos = sum(1 for t in tokens if t in _POS_WORDS)
    neg = sum(1 for t in tokens if t in _NEG_WORDS)
    total = pos + neg
    if total == 0:
        score = 0.0
    else:
        score = (pos - neg) / float(total)

    if score > 0.15:
        label = "positivo"
    elif score < -0.15:
        label = "negativo"
    else:
        label = "neutral"

    tone = ""
    for pattern, name in _TONE_MAP:
        if pattern.search(text):
            tone = name
            break

    return Sentiment(label=label, score=round(score, 3), tone=tone)
