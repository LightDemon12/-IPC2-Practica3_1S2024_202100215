from flask import Flask, request, jsonify, render_template, send_file , Response
from flask_cors import CORS
import xml.etree.ElementTree as ET
from Logica.Estructura import Animal
from Logica.XML_Reader import read_xml, filter_animals, create_xml
from xml.dom import minidom
import os

import re

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
        count_element = ET.SubElement(animal_element, 'CantidadTotal')
        count_element.text = str(count)
    
    xml_string = ET.tostring(root, encoding='utf8', method='xml')
    dom = minidom.parseString(xml_string)
    xml_str = dom.toprettyxml(encoding='utf-8')  # Utiliza toprettyxml() para agregar tabulaciones

    # Elimina las líneas en blanco adicionales
    xml_pretty_str = re.sub(r'>\n\s+([^<>\s].*?)\n\s+</', r'>\1<', xml_str.decode())

    with open('../Archivos/resultados.xml', 'wb') as f:
        f.write(xml_pretty_str.encode('utf-8'))

    return ET.tostring(root, encoding='utf8', method='xml')
    return xml_pretty_str

@app.route('/process', methods=['GET'])
def process_file():
    # Aquí puedes procesar el archivo XML y devolver los resultados
    response = {
        'message': 'File successfully processed'
    }
    return jsonify(response), 200

from xml.etree import ElementTree as ET

@app.route('/results', methods=['GET'])
def get_results():
    animalesresult= []
    for animal in animales:
        animal_dict = {
            'tipo': animal.tag,
            'raza': animal.findtext('raza'),
            'edad': animal.findtext('edad')
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






@app.route('/download', methods=['GET'])
def download_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../Archivos/resultados.xml')
    response = send_file(file_path, as_attachment=True)
    response.headers["Content-Disposition"] = "attachment; filename=resultados.xml"
    return response

if __name__ == '__main__':
    app.run(host='localhost', port='5000',debug=True)