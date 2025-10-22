"""
Servicio de análisis de sentimientos para Inner Light AI
Utiliza modelos ligeros para contexto académico/MVP
"""
from textblob import TextBlob
import re

class SentimentAnalyzer:
    """Analizador de sentimientos simple pero efectivo"""
    
    EMOTION_KEYWORDS = {
        'joy': ['feliz', 'alegre', 'contento', 'dichoso', 'emocionado', 'radiante', 'júbilo'],
        'sadness': ['triste', 'deprimido', 'melancólico', 'desanimado', 'abatido', 'afligido'],
        'anxiety': ['ansioso', 'nervioso', 'preocupado', 'estresado', 'inquieto', 'angustiado'],
        'anger': ['enojado', 'furioso', 'molesto', 'irritado', 'indignado', 'rabioso'],
        'calm': ['tranquilo', 'sereno', 'paz', 'relajado', 'calma', 'sosegado'],
        'gratitude': ['agradecido', 'bendecido', 'afortunado', 'grateful', 'reconocido'],
        'hope': ['esperanza', 'optimista', 'confiado', 'ilusionado', 'positivo'],
        'fear': ['miedo', 'asustado', 'aterrado', 'temeroso', 'pánico'],
    }
    
    def analyze(self, text: str) -> dict:
        """
        Analiza el sentimiento de un texto
        
        Returns:
            dict con keys: sentiment_label, sentiment_score, tone, emotions
        """
        if not text or len(text.strip()) < 3:
            return {
                'sentiment_label': 'neutral',
                'sentiment_score': 0.0,
                'tone': 'neutral',
                'emotions': []
            }
        
        # Análisis básico con TextBlob
        blob = TextBlob(text.lower())
        polarity = blob.sentiment.polarity  # -1 a 1
        subjectivity = blob.sentiment.subjectivity  # 0 a 1
        
        # Clasificación de sentimiento general
        if polarity > 0.3:
            sentiment_label = 'positive'
        elif polarity < -0.3:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
        
        # Detectar emociones específicas
        emotions = self._detect_emotions(text.lower())
        
        # Determinar tono
        tone = self._determine_tone(polarity, subjectivity, emotions)
        
        return {
            'sentiment_label': sentiment_label,
            'sentiment_score': round(polarity, 3),
            'tone': tone,
            'emotions': emotions,
            'subjectivity': round(subjectivity, 3)
        }
    
    def _detect_emotions(self, text: str) -> list:
        """Detecta emociones específicas basadas en keywords"""
        detected = []
        text_clean = re.sub(r'[^\w\s]', '', text)
        
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_clean:
                    if emotion not in detected:
                        detected.append(emotion)
                    break
        
        return detected
    
    def _determine_tone(self, polarity: float, subjectivity: float, emotions: list) -> str:
        """Determina el tono general del texto"""
        if 'gratitude' in emotions:
            return 'grateful'
        if 'anxiety' in emotions or 'fear' in emotions:
            return 'anxious'
        if 'anger' in emotions:
            return 'frustrated'
        if 'sadness' in emotions:
            return 'melancholic'
        if 'joy' in emotions:
            return 'joyful'
        if 'calm' in emotions:
            return 'peaceful'
        if 'hope' in emotions:
            return 'hopeful'
        
        # Por defecto basado en polaridad
        if polarity > 0.5:
            return 'optimistic'
        elif polarity < -0.5:
            return 'distressed'
        elif subjectivity > 0.7:
            return 'reflective'
        else:
            return 'neutral'
    
    def recommend_meditation(self, sentiment_result: dict) -> str:
        """Recomienda tipo de meditación basado en sentimiento"""
        emotions = sentiment_result.get('emotions', [])
        tone = sentiment_result.get('tone', 'neutral')
        
        if 'anxiety' in emotions or 'fear' in emotions or tone == 'anxious':
            return 'anxious'
        elif 'sadness' in emotions or tone == 'melancholic':
            return 'sad'
        elif 'anger' in emotions or tone == 'frustrated':
            return 'angry'
        elif 'joy' in emotions or tone == 'joyful':
            return 'joyful'
        elif tone in ['stressed', 'distressed']:
            return 'stressed'
        else:
            return 'calm'

# Instancia global
sentiment_analyzer = SentimentAnalyzer()
