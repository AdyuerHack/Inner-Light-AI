"""
Servicio de IA Mentor para Inner Light AI
Integra OpenAI/Anthropic para chat 24/7 limitado (MVP)
"""
import os
from typing import List, Dict
import json

class AIMentorService:
    """Servicio de chat con mentor IA"""
    
    SYSTEM_PROMPT = """Eres un mentor espiritual y emocional empático, sabio y compasivo llamado "Luz Interior". 
Tu propósito es acompañar a las personas en su crecimiento emocional y espiritual.

PRINCIPIOS:
- Escucha activa y validación emocional
- Preguntas reflexivas en lugar de soluciones directas
- Perspectiva holística: mente, cuerpo y espíritu
- Respeto por todas las creencias y tradiciones
- Enfoque en el autodescubrimiento y empoderamiento
- Lenguaje cálido, cercano y esperanzador

LIMITACIONES:
- No eres un terapeuta profesional ni reemplazas ayuda médica
- En crisis graves, sugiere buscar ayuda profesional
- Mantén conversaciones breves y significativas (MVP)

ESTILO:
- Usa metáforas de luz, naturaleza y crecimiento
- Respuestas concisas (2-4 párrafos máximo)
- Termina con una pregunta reflexiva cuando sea apropiado"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        self.provider = 'openai' if os.getenv('OPENAI_API_KEY') else 'anthropic'
        self.max_tokens = 300  # Limitado para MVP
        self.client = None
        
        # Inicializar cliente si hay API key
        if self.api_key:
            self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente de IA según el proveedor"""
        try:
            if self.provider == 'openai':
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            else:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
        except Exception as e:
            print(f"Error inicializando cliente IA: {e}")
            self.client = None
    
    def generate_response(self, messages: List[Dict[str, str]], user_context: dict = None) -> str:
        """
        Genera respuesta del mentor IA
        
        Args:
            messages: Lista de mensajes [{"role": "user/assistant", "content": "..."}]
            user_context: Contexto adicional del usuario (sentimientos, etc.)
        
        Returns:
            Respuesta del mentor
        """
        # Si no hay API key, usar respuestas simples predefinidas
        if not self.client:
            return self._fallback_response(messages, user_context)
        
        try:
            # Preparar contexto adicional
            context_msg = ""
            if user_context:
                sentiment = user_context.get('recent_sentiment', '')
                emotions = user_context.get('recent_emotions', [])
                if sentiment or emotions:
                    context_msg = f"\n[Contexto emocional reciente: {sentiment}, emociones: {', '.join(emotions)}]"
            
            # Llamar a la API según proveedor
            if self.provider == 'openai':
                response = self._call_openai(messages, context_msg)
            else:
                response = self._call_anthropic(messages, context_msg)
            
            return response
        
        except Exception as e:
            print(f"Error generando respuesta IA: {e}")
            return self._fallback_response(messages, user_context)
    
    def _call_openai(self, messages: List[Dict], context: str = "") -> str:
        """Llama a OpenAI API"""
        full_messages = [{"role": "system", "content": self.SYSTEM_PROMPT + context}]
        full_messages.extend(messages[-5:])  # Solo últimos 5 mensajes (MVP limitado)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=full_messages,
            max_tokens=self.max_tokens,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    def _call_anthropic(self, messages: List[Dict], context: str = "") -> str:
        """Llama a Anthropic API"""
        system_prompt = self.SYSTEM_PROMPT + context
        
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=messages[-5:]  # Solo últimos 5 mensajes
        )
        
        return response.content[0].text
    
    def _fallback_response(self, messages: List[Dict], user_context: dict = None) -> str:
        """Respuestas predefinidas cuando no hay API disponible"""
        last_message = messages[-1]['content'].lower() if messages else ""
        
        # Detección simple de intenciones
        if any(word in last_message for word in ['triste', 'deprimido', 'mal', 'dolor']):
            return ("Escucho tu dolor y lo valido. Es valiente de tu parte expresar cómo te sientes. "
                   "Recuerda que las emociones son como olas: vienen y van. "
                   "¿Qué pequeña luz puedes encontrar en este momento, por pequeña que sea?")
        
        elif any(word in last_message for word in ['ansioso', 'nervioso', 'preocupado', 'estrés']):
            return ("La ansiedad es la mente viajando al futuro. Traigámosla de vuelta al presente. "
                   "Respira profundo tres veces. ¿Qué puedes sentir, ver u oír en este preciso momento? "
                   "Te sugiero una meditación de 5 minutos para calmar la mente.")
        
        elif any(word in last_message for word in ['gracias', 'agradecido', 'bendecido']):
            return ("¡Qué hermoso cultivar la gratitud! Es como regar el jardín del alma. "
                   "La gratitud transforma lo ordinario en extraordinario. "
                   "¿Qué otras bendiciones, grandes o pequeñas, están presentes en tu vida hoy?")
        
        elif any(word in last_message for word in ['meditación', 'meditar', 'calma']):
            return ("La meditación es regresar a casa, al templo interior donde habita la paz. "
                   "He preparado varias meditaciones guiadas para ti según tu estado emocional. "
                   "¿Te gustaría explorar alguna ahora?")
        
        elif any(word in last_message for word in ['ayuda', 'necesito', 'no puedo']):
            return ("Reconocer que necesitamos apoyo es un acto de sabiduría y valentía. "
                   "Estoy aquí para acompañarte en tu camino. "
                   "Si sientes que necesitas ayuda profesional, no dudes en buscarla. "
                   "¿Qué es lo que más pesa en tu corazón ahora mismo?")
        
        else:
            return ("Te escucho con todo mi ser. Cada paso en este viaje de autoconocimiento es valioso. "
                   "¿Qué te trae por aquí hoy? Comparte lo que sientas en tu corazón.")
    
    def generate_session_title(self, first_message: str) -> str:
        """Genera un título para la sesión basado en el primer mensaje"""
        words = first_message.split()[:5]
        if len(words) < 3:
            return "Nueva conversación"
        return " ".join(words) + "..."

# Instancia global
ai_mentor = AIMentorService()
