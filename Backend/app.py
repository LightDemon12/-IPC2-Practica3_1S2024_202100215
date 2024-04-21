from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import xml.etree.ElementTree as ET
from Logica.Estructura import Animal
from Logica.XML_Reader import read_xml, filter_animals, create_xml

app = Flask(__name__)
CORS(app)

animales = []
contadores = {'perro': 0, 'gato': 0, 'conejo': 0}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

def procesar_elemento(elemento):
    tipo_animal = elemento.tag
    if tipo_animal in ['perro', 'gato', 'conejo']:
        contadores[tipo_animal] += 1
        animales.append(elemento)  # Agrega el animal a la lista de animales

@app.route('/upload', methods=['POST'])
def upload_file():
    entradaXML = request.data
    decodificarXML= entradaXML.decode('utf-8')
    print(decodificarXML)
    
    xmlRecibido = ET.XML(decodificarXML)

    for animal in xmlRecibido:
        procesar_elemento(animal)

    root = ET.Element('resultados')
    animales_element = ET.SubElement(root, 'animales')
    for animal, count in contadores.items():
        animal_element = ET.SubElement(animales_element, animal)
        animal_element.text = str(count)
    
    return ET.tostring(root, encoding='utf8', method='xml')


@app.route('/process', methods=['GET'])
def process_file():
    # Aquí puedes procesar el archivo XML y devolver los resultados
    response = {
        'message': 'File successfully processed'
    }
    return jsonify(response), 200


@app.route('/results', methods=['GET'])
def get_results():
    animalesresult= []
    for animal in animales:
        animal_dict = {
            'tag': animal.tag,
            'attributes': animal.attrib,
            'text': animal.text
        }
        animalesresult.append(animal_dict)
    return jsonify(animalesresult)

@app.route('/clear', methods=['DELETE'])
def clear_animals():
    animales.clear()  # Borra todos los elementos de la lista
    contadores['perro'] = 0  # Restablece los contadores
    contadores['gato'] = 0
    contadores['conejo'] = 0
    return jsonify({'message': 'Animales cleared'}), 200


if __name__ == '__main__':
    app.run(host='localhost', port='5000',debug=True)