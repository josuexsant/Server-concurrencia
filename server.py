from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from lxml import etree
import os

def search_dir(directory_path):
    if os.path.isdir(directory_path):
        try:
            contents = os.listdir(directory_path)
            return {'status': 200, 'contents': contents if contents else ""}
        except Exception as e:
            return {'status': 500, 'message': f"Error al listar el contenido del directorio: {e}"}
    else:
        return {'status': 404, 'message': "El directorio no existe"}

def handle_soap_request(request):
    try:
        envelope = etree.fromstring(request)
        namespace = {'soap': 'http://www.w3.org/2003/05/soap-envelope', 'ns': 'http://example.com/directoryservice'}
        path = envelope.xpath('//ns:Path', namespaces=namespace)[0].text
        result = search_dir(path)
        
        response = etree.Element('{http://www.w3.org/2003/05/soap-envelope}Envelope')
        body = etree.SubElement(response, '{http://www.w3.org/2003/05/soap-envelope}Body')
        response_body = etree.SubElement(body, '{http://example.com/directoryservice}GetDirectoryContentsResponse')
        status = etree.SubElement(response_body, 'Status')
        status.text = str(result['status'])
        
        items = etree.SubElement(response_body, 'Items')
        if 'contents' in result:
            for item in result['contents']:
                item_element = etree.SubElement(items, 'Item')
                item_element.text = item
        else:
            message = etree.SubElement(items, 'Message')
            message.text = result['message']
        response_xml = etree.tostring(response, encoding='unicode', pretty_print=True)
        print("Respuesta XML generada:", response_xml)
        return etree.tostring(response, encoding='unicode', pretty_print=True)
    except Exception as e:
        print(f"Error al procesar la solicitud SOAP: {e}")
        return "<error>Internal Server Error</error>"

with SimpleXMLRPCServer(('127.0.0.1', 8000), requestHandler=SimpleXMLRPCRequestHandler) as server:
    server.register_function(handle_soap_request, 'handleSoapRequest')
    print('Servidor en ejecución en el puerto 8000...')
    server.serve_forever()