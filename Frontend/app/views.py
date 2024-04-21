from django.shortcuts import render
import requests
from .forms import FileForm
from xml.dom.minidom import parseString 
import re


API = 'http://localhost:5000'



# Create your views here.
def index (request):
    return render(request, 'index.html')

def ayuda(request):
    return render(request, 'ayuda.html')

def Carga (request):
    return render(request, 'Carga.html')

def revisión(request):
    return render(request, 'Revision.html')



def cargarXML(request):
    context = {
        'content': None
    }

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            txt = uploaded_file.read() # Lee el contenido del archivo
            response = requests.post('http://localhost:5000/upload', data=txt)  # Cambia API+'/results' a 'http://localhost:5000/upload'
            if response.status_code == 200:
                xml_response = response.text  # Lee la respuesta como texto
                dom = parseString(xml_response)  # Parsea el XML
                pretty_xml = dom.toprettyxml()  # Serializa el XML con indentación
                context['content'] = pretty_xml  # Guarda la respuesta XML en el contexto
                return render(request, 'Carga.html', context)
        return render(request, 'Carga.html')
    else:
        return render(request, 'Carga.html')

def clear_animals(request):
    response = requests.delete('http://localhost:5000/clear')
    if response.status_code == 200:
        return render(request, 'clear_success.html', {'alert_message': '¡Bien hecho! Las mascotas se han borrado con éxito.'})
    else:
        return render(request, 'clear_error.html', {'alert_message': '¡Error! Hubo un problema al intentar borrar las mascotas.'})

def posts(request):
    context = {
        'posts': None
    }
    response = requests.get('http://localhost:5000/results')
    if response.status_code == 200:
        context['posts'] = response.json()
        return render(request, 'Revision.html', context)
    else:
        return render(request, 'Revision.html')

def download(request):
    context = {
        'content': None
    }

    response = requests.get('http://localhost:5000/download')
    if response.status_code == 200:
        xml_response = response.text  # Lee la respuesta como texto
        dom = parseString(xml_response)  # Parsea el XML
        pretty_xml = dom.toprettyxml()  # Serializa el XML con indentación
        pretty_xml = re.sub(r'\n\s*\n', '\n', pretty_xml)  # Elimina espacios en blanco adicionales
        context['content'] = pretty_xml  # Guarda la respuesta XML en el contexto
        return render(request, 'Carga.html', context)
    else:
        return render(request, 'Carga.html')