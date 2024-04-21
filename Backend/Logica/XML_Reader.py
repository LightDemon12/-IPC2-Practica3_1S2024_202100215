import xml.etree.ElementTree as ET
from Logica.Estructura import Animal

def read_xml(file):
    # Parsea el archivo XML
    tree = ET.parse(file)
    root = tree.getroot()

    # Crea una lista para almacenar los animales
    animales = []

    # Itera sobre cada animal en el archivo XML
    for animal in root:
        # Crea una instancia de Animal
        animal_instance = Animal(animal.tag, animal.find('edad').text, animal.find('raza').text)

        # Agrega la instancia a la lista de animales
        animales.append(animal_instance)

    # Devuelve la lista de animales
    return animales


def filter_animals(animales):
    # Crea una lista para almacenar los animales filtrados
    animales_filtrados = []

    # Itera sobre cada animal en la lista
    for animal in animales:
        # Si el tipo de animal es 'Perro', 'Gato' o 'Conejo', agrega el animal a la lista filtrada
        if animal.tipo in ['Perro', 'Gato', 'Conejo']:
            animales_filtrados.append(animal)

    # Devuelve la lista de animales filtrados
    return 

def create_xml(animales):
    # Crea el elemento raíz
    resultados = ET.Element('resultados')

    # Crea el subelemento 'animales'
    animales_element = ET.SubElement(resultados, 'animales')

    # Crea los subelementos para cada tipo de animal
    for tipo in ['perros', 'gatos', 'conejos']:
        # Cuenta la cantidad de animales de este tipo
        cantidad = sum(1 for animal in animales if animal.tipo.lower() == tipo[:-1])

        # Crea el subelemento para este tipo de animal
        animal_element = ET.SubElement(animales_element, tipo)
        cantidad_element = ET.SubElement(animal_element, 'cantidad')
        cantidad_element.text = str(cantidad)

    # Crea el árbol XML y escribe el archivo
    tree = ET.ElementTree(resultados)
    tree.write('resultados.xml', encoding='utf-8', xml_declaration=True)


