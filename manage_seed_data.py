#!/usr/bin/env python3
"""
Script para poblar la base de datos con meditaciones iniciales
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innerlight.settings')
django.setup()

from apps.meditation.models import Meditation

def create_meditations():
    """Crear meditaciones guiadas de ejemplo"""
    
    meditations_data = [
        {
            'title': 'Respiración para la Calma',
            'description': 'Una meditación simple enfocada en la respiración para encontrar paz interior.',
            'emotion_target': 'calm',
            'duration_minutes': 5,
            'script': '''Encuentra una posición cómoda y cierra suavemente los ojos.

Toma una respiración profunda por la nariz... y exhala lentamente por la boca.

Siente cómo tu cuerpo se relaja con cada exhalación.

Inhala contando hasta 4... 1, 2, 3, 4...
Sostén por 2... 1, 2...
Exhala contando hasta 6... 1, 2, 3, 4, 5, 6...

Continúa con este ritmo natural. Si tu mente divaga, gentilmente tráela de vuelta a tu respiración.

Eres como un lago tranquilo. Las ondas en la superficie se calman, revelando la profundidad pacífica debajo.

Permanece aquí, respirando, siendo.'''
        },
        {
            'title': 'Liberando la Ansiedad',
            'description': 'Técnicas de anclaje y respiración para momentos de ansiedad.',
            'emotion_target': 'anxious',
            'duration_minutes': 10,
            'script': '''La ansiedad es la mente viajando al futuro. Vamos a traerla de vuelta al presente.

Primero, reconoce tu ansiedad. "Estoy sintiendo ansiedad, y eso está bien."

Ahora, anclémonos al momento presente:
- Nombra 5 cosas que puedes VER
- 4 cosas que puedes TOCAR
- 3 cosas que puedes ESCUCHAR
- 2 cosas que puedes OLER
- 1 cosa que puedes SABOREAR

Respira profundamente. El aire entra limpio y fresco. Sale llevándose la tensión.

Imagina que cada preocupación es una nube flotando en el cielo. Las observas pasar, pero no te aferras a ellas.

Aquí y ahora, en este momento, estás seguro. Respira en esta verdad.'''
        },
        {
            'title': 'Luz en la Tristeza',
            'description': 'Una meditación compasiva para momentos de tristeza.',
            'emotion_target': 'sad',
            'duration_minutes': 10,
            'script': '''La tristeza es parte del ser humano. No la rechaces, acógela con compasión.

Imagina que tu tristeza es un niño pequeño. ¿Qué le dirías? ¿Cómo lo consolarías?

Coloca una mano sobre tu corazón. Siente su calor.

Repite suavemente: "Estoy aquí para mí. Me permito sentir. Esto también pasará."

Visualiza una luz dorada y cálida en tu corazón. Con cada respiración, esta luz crece.

La luz no niega la oscuridad, simplemente la acompaña. Pueden coexistir.

Recuerda un momento en que te sentiste amado, seguro, en paz. Ese sentimiento sigue dentro de ti.

La tristeza es una estación, no tu destino permanente.'''
        },
        {
            'title': 'Enfriando el Fuego Interior',
            'description': 'Meditación para transformar el enojo en comprensión.',
            'emotion_target': 'angry',
            'duration_minutes': 10,
            'script': '''El enojo es energía. No es malo, es señal de que algo importa.

Pero, ¿qué hay debajo del enojo? ¿Dolor? ¿Miedo? ¿Necesidad no satisfecha?

Respira en el fuego. No para apagarlo, sino para entenderlo.

Imagina que el enojo es un volcán. En lugar de reprimir o explotar, lo observamos.

Con cada exhalación, el calor se transforma. Rojo intenso... naranja... amarillo... blanco cálido.

Pregúntale a tu enojo: "¿Qué necesitas que yo sepa?"

La respuesta puede sorprenderte. Escucha con compasión.

Eres más grande que tu enojo. Puedes sostenerlo sin ser controlado por él.'''
        },
        {
            'title': 'Amplificando la Alegría',
            'description': 'Meditación para saborear y expandir momentos de alegría.',
            'emotion_target': 'joyful',
            'duration_minutes': 5,
            'script': '''¡Qué regalo estar experimentando alegría!

Tómate un momento para realmente sentirla. ¿Dónde vive en tu cuerpo?

¿Es una chispa en tu pecho? ¿Una ligereza en tus hombros? ¿Una sonrisa en tu corazón?

Respira en esta alegría. Con cada inhalación, crece. Con cada exhalación, se expande.

Imagina que esta alegría es luz. Llena tu cuerpo, luego se desborda hacia el mundo.

Envía esta luz a alguien que amas. A un extraño en la calle. Al planeta entero.

La alegría compartida se multiplica. Guardada con gratitud, perdura.

Gracias por este momento. Gracias por estar vivo. Gracias por la capacidad de sentir alegría.'''
        },
        {
            'title': 'Sanando el Estrés',
            'description': 'Escaneo corporal y liberación de tensión para días estresantes.',
            'emotion_target': 'stressed',
            'duration_minutes': 15,
            'script': '''El estrés vive en el cuerpo. Vamos a liberarlo, parte por parte.

Empieza con tu rostro. ¿Está tu mandíbula apretada? Afloja. Suaviza las cejas.

Tus hombros. Los llevas tan arriba. Déjalos caer, caer, caer.

Respira en tu pecho. Con cada exhalación, crea más espacio.

Tu estómago. ¿Está en nudos? Imagina que se desenreda, se relaja.

Tus manos. ¿Están en puños? Ábrelas. Sacude los dedos.

Tus piernas, tus pies. Pesados, apoyados, seguros en la tierra.

Ahora imagina una cascada de luz sanadora fluyendo desde tu coronilla hasta tus pies.

Lleva consigo todo el estrés, toda la tensión, toda la preocupación.

Lo que queda es tú, en tu estado natural: en paz, presente, completo.'''
        },
        {
            'title': 'Meditación de Balance',
            'description': 'Para días neutrales, cultivando presencia y equilibrio.',
            'emotion_target': 'neutral',
            'duration_minutes': 10,
            'script': '''En este momento de neutralidad, hay una invitación.

No estás en alto ni en bajo. Estás en el centro, en el punto de equilibrio.

Desde aquí, puedes ver con claridad. El pasado, el futuro, pero sobre todo el ahora.

Respira naturalmente. No fuerces nada. Solo sé.

Observa los pensamientos como pájaros cruzando el cielo. Vienen, van.

Observa las sensaciones en tu cuerpo. Cambian constantemente.

Observa las emociones. Como el clima, siempre en flujo.

Pero hay algo en ti que observa todo esto. Algo constante, pacífico, sabio.

Ese observador eres tú en tu esencia. Siempre presente, nunca perturbado.

Descansa en esta conciencia. Este es tu hogar interior.'''
        },
        {
            'title': 'Conexión con la Tierra',
            'description': 'Meditación de enraizamiento y conexión con la naturaleza.',
            'emotion_target': 'calm',
            'duration_minutes': 10,
            'script': '''Imagina que eres un árbol. Fuerte, arraigado, en paz.

Tus pies son raíces que se hunden profundamente en la tierra.

Siente cómo estas raíces te conectan con el planeta, con la vida misma.

Tu torso es el tronco. Estable, sólido, capaz de balancearse con el viento sin quebrarse.

Tus brazos son ramas que se extienden hacia el cielo, recibiendo la luz del sol.

Las hojas de tu árbol son tus pensamientos. Vienen en primavera, caen en otoño.

Pero tú, el árbol, permaneces. Temporada tras temporada, año tras año.

Respira con la tierra. Inhala su energía. Exhala tu gratitud.

Eres parte de algo mucho más grande. Y eso te sostiene.'''
        },
    ]
    
    print("Creando meditaciones...")
    for data in meditations_data:
        meditation, created = Meditation.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"✓ Creada: {meditation.title}")
        else:
            print(f"- Ya existe: {meditation.title}")
    
    print(f"\n¡Completado! Total de meditaciones: {Meditation.objects.count()}")

if __name__ == '__main__':
    create_meditations()
