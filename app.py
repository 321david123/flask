from flask import Flask, render_template, request, jsonify
import random
app = Flask(__name__)

# Ruta para cargar la página principal
@app.route('/')
def index():
    return render_template('./index.html')

import difflib

# Diccionario de intenciones y respuestas
intenciones = {
    "¡Hola! ¿En qué puedo ayudarte?": ["Hola", "Holi", "Saludos", "Klk", "Jelow", "ola", "oli"],
    "Adios, un gusto haberte ayudado, si tienes alguna otra duda hazmela llegar": ["Adiós", "Hasta luego", "¡Hasta pronto!","Bye", "Ahi nos vidrios"],
    "Sal y compruebalo tu mismo :3": ["¿Cómo está el clima hoy?", "Dime cómo está el tiempo", "¿Qué tiempo hace?"],
    "Porque no revisas las UnoNoticias": ["Cuéntame las últimas noticias", "Noticias recientes", "¿Qué hay de nuevo?"],
    "Se produce una disminución de la cantidad de iones carbonato en el agua, un elemento necesario para la formación de los esqueletos y las conchas de ciertos animales marinos. Por tanto, esta situación podría afectar a su desarrollo y a su capacidad de reproducción, poniendo en peligro sus poblaciones.": ["cuales son las consecuencias de la acidificacion?", "Cuales son las consecuencias de la acidificiacion?", "Kuales son las consecuencias de la acidificacion?", "Puedes decirme las consecuencias de la acidificacion?", "Dime las consecuencias de la acidificacion", "Consecuencias de la acidificacion"],
    "Las aguas costeras son las aguas marinas situadas entre las aguas oceánicas y el continente, y se caracterizan por tener una influencia notable de las aguas continentales (ríos, rieras, pantanales, acuíferos...). ": ["que son las aguas costeras?", "q son las aguas costeras?","Q son las aguas costeras","q son las aguas costeras","Aguas costeras","que es aguas costeras","aguas costeras"],
    "Algunos de los contaminantes más comunes derivados de la actividad humana son los plaguicidas, herbicidas, fertilizantes químicos, detergentes, hidrocarburos, aguas residuales, plásticos y otros sólidos. ": ["cual es el principal contaminante de las aguas?","Dime el principal contaminante de las aguas costeras","Que contamina las aguas costeras?","Q contamina las aguas costeras?","Contaminantes de las aguas costeras"],
    "La pesquería es la agrupación de hombres, embarcaciones y equipos de pesca para la explotación de un determinado recurso en un área concreta. La pesquería comprende a las unidades de pesca y a la unidad o unidades de stock.": ["q es una pesqueria?","Q es pesqueria?","q es pesqueria","que es la pesqueria?","Dime que es una pesqueria?","Puedes decirme que es una pesqueria?","dime que es una pesqueria"],
    "La eutrofización se refiere al aporte en exceso de nutrientes inorgánicos (procedentes de actividades humanas), principalmente Nitrógeno (N) y Fósforo (P), en un ecosistema acuático, produciendo una proliferación descontrolada de algas fitoplanctónicas y provocando efectos adversos en las masas de agua afectadas.": ["que es eutrofizacion?","Q es eutrofizacion?","q es autofrizacion","q es autofrizacion?","Que es autofrizacion?","Dime que es la autofrizacion","dime que es la autofrizacion","que es eso de autofrizacion?","Dime que es autofrizacion"],
    "La vida marina conforman las plantas, los animales y otros organismos que viven en el agua salada de los mares y océanos, o el agua salobre de los estuarios costeros.": ["q es vida sumbarina?","Que es vida submarina","q es vida submarina","Que es vida submarina?","Vida submarina","define vida submarina","Dime que es la vida submarina","Que significa vida submarina?","QUE ES LA VIDA SUBMARINA?"],
    "La acidificación del océano se define como una disminución del pH del océano durante décadas o más que es causada principalmente por la absorción de dióxido de carbono (CO2) de la atmósfera.": ["q es acidificacion?","Que es acidificacion?","QUE ES ACIDIFICACION?","define acidificacion","Dime que es acidificacion","Acidificacion","q es acidificacion"],
    "¡Un gusto!, me presento mi nombre es IAn la Red Neuronal de Linuxeros72": ["¿Cuál es tu nombre?", "kual es tu nombre", "como te llamas?", "komo te llamas", "kien eres", "quien eres", "quien eres tu" ],
    "Por en momento unicamente hablo Español Latino pero más adelante podria hablar algunos otros": ["¿En qué idiomas puedes comunicarte?", "¿Hablas ingles?", "Halblas frances", "Hablas en algun otro idioma?"],
    "Puedo resolver algunas dudas sobre la Vida Submarina, y ¿porque no? charlar un rato contigo": ["¿Cuál es tu función principal?", "kual es tu funcion principal", "pa que eres bueno", "que sabes hacer", "para que fuiste creado?"],
    "Puedes leer La Teoria de la Relatividad de Cristhian Daniel Gaona": ["¿Puedes recomendarme un libro?","algun libro que recomiendes", "un libro que te guste mucho?"],
    "Puedes ver Five Nights At Freddys este Miercoles 25 de Octubre, solo en Cines...": ["¿Puedes recomendarme una película popular?","alguna pelicula que recomiendes", "una pelicula que te guste mucho?"],
    "Pues si no hay alguien cerca que te pueda proporcionar uno, una calceta seria una buena alternativa": ["¿que hago si no hay papel en el baño?", "que hago si estoy solo y no hay papel?", "no hay papel en el baño" ],
    "No puedo sentir emociones ya que al ser un ChatBot no cuento con ellas": ["¿Conoces los sentimientos?", "tienes sentimientos?"],



    }

# Función para determinar la intención del usuario
def get_response(texto):
    texto = texto.lower()
    print("estamos aqui")
    mejor_coincidencia = None
    mejor_ratio = 0

    # Buscar la mejor coincidencia en las intenciones
    for intencion, respuestas in intenciones.items():
        print('respuestas')
        for respuesta in respuestas:
            ratio = difflib.SequenceMatcher(None, texto, respuesta.lower()).ratio()
            if ratio > mejor_ratio:
                mejor_ratio = ratio
                mejor_coincidencia = intencion

    if mejor_ratio > 0.4:  # Umbral de ratio para la coincidencia
        return mejor_coincidencia
    else:
        return "otra_pregunta"

# Función para responder a la pregunta del usuario
def responder_pregunta(texto):
    intencion = get_response(texto)
    respuestas = intenciones[intencion]
    print('obtenemos respuesta')
    return random.choice(respuestas)

# Ejemplo de uso

# Ruta para procesar las solicitudes de los usuarios
@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    ai_response = responder_pregunta(user_message)
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
