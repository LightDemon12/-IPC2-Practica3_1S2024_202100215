from django.shortcuts import render
import requests
from .forms import FileForm
from xml.dom.minidom import parseString


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
            txt = uploaded_file.read().decode('utf-8')  # Lee el contenido del archivo
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