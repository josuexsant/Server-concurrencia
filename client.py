import socket
import xml.etree.ElementTree as ET

class Client:
    middleware_port = 8080
    middleware_ip = '127.0.0.1'
    
    def __init__(self, path):
        self.path = path
        self.print_response()  # Llamar a print_response directamente en el constructor
        
    def request(self):
        soap_message = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
        <soap:Header>
        </soap:Header>
        <soap:Body>
            <GetDirectoryContents xmlns="http://example.com/directoryservice">
            <Path>{self.path}</Path>
            </GetDirectoryContents>
        </soap:Body>
        </soap:Envelope>"""
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.middleware_ip, self.middleware_port))
                client_socket.sendall(soap_message.encode('utf-8'))
                response = client_socket.recv(4096).decode('utf-8')  # Aumenté el buffer a 4096
                return response
        except Exception as e:
            print(f"Error al conectar con el middleware: {e}")
            return None
        
    def parse_response(self, response):
        try:
            # Imprime la respuesta para depuración
            print("Respuesta recibida:", response)

            # Parsear el XML
            root = ET.fromstring(response)
            
            # Definir los namespaces
            namespaces = {
                'soap': 'http://www.w3.org/2003/05/soap-envelope',
                'ns1': 'http://example.com/directoryservice'
            }
            
            # Buscar el cuerpo de la respuesta SOAP
            body = root.find('soap:Body', namespaces)
            if body is None:
                raise ValueError("No se encontró el elemento 'Body' en la respuesta SOAP.")
            
            # Buscar la respuesta específica
            response_element = body.find('ns1:GetDirectoryContentsResponse', namespaces)
            if response_element is None:
                raise ValueError("No se encontró el elemento 'GetDirectoryContentsResponse' en la respuesta SOAP.")
            
            # Extraer el estado
            status = response_element.find('ns1:Status', namespaces)
            if status is None:
                raise ValueError("No se encontró el elemento 'Status' en la respuesta SOAP.")
            
            # Extraer los elementos
            items = response_element.find('ns1:Items', namespaces)
            if items is None:
                raise ValueError("No se encontró el elemento 'Items' en la respuesta SOAP.")
            
            # Crear la lista de elementos
            item_list = [item.text for item in items.findall('ns1:Item', namespaces)]
            
            return status.text, item_list
        except Exception as e:
            print(f"Error al parsear la respuesta: {e}")
            return None, None

    def print_response(self):
        response = self.request()
        if response:
            status, items = self.parse_response(response)
            if status and items:
                print("-" * 50)
                print(f"Status: {status}")
                print("Items:")
                for item in items:
                    print(f" - {item}")
                print("-" * 50)
            else:
                print("No se pudo obtener una respuesta válida.")