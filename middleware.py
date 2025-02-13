import socket
import time
import xmlrpc.client
import threading
from xml.etree import ElementTree as ET

def middleware(request, client_address):
    request_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("=" * 50)
    print(request_time + f" : Request from {client_address[0]}")
    print(f"Request: {request}")
    
    # Parse the SOAP request
    try:
        envelope = ET.fromstring(request)
        namespaces = {'soap': 'http://www.w3.org/2003/05/soap-envelope', 'ns': 'http://example.com/directoryservice'}
        body = envelope.find('soap:Body', namespaces)
        get_directory_contents = body.find('ns:GetDirectoryContents', namespaces)
        path = get_directory_contents.find('ns:Path', namespaces).text
    except ET.ParseError as e:
        print(f"Error parsing SOAP request: {e}")
        return 400, "Bad Request"
    except AttributeError as e:
        print(f"Error processing SOAP request: {e}")
        return 400, "Bad Request"

    # Conexión con el servidor XML-RPC local
    server_ip = '127.0.0.1'  # Servidor está en la misma máquina
    server_port = 8000       # Puerto del servidor XML-RPC
    proxy = xmlrpc.client.ServerProxy(f'http://{server_ip}:{server_port}')
    try:
        response = proxy.handleSoapRequest(request)
    except xmlrpc.client.Fault as e:
        print(f"XML-RPC Fault: {e}")
        return 500, "Internal Server Error"
    except Exception as e:
        print(f"Error al conectar con el servidor XML-RPC: {e}")
        return 500, "Internal Server Error"
    print("Respuesta del servidor:", response)       
    return 200, response

def handle_request(client_socket, client_address):
    """Maneja la solicitud del cliente."""
    try:
        # Recibir los datos de la solicitud
        request = client_socket.recv(4096).decode('utf-8')  # Aumenté el buffer a 4096

        # Procesar la solicitud mediante el middleware
        status_code, response_message = middleware(request, client_address)

        # Enviar la respuesta al cliente
        response = f"HTTP/1.1 {status_code} {'OK' if status_code == 200 else 'Error'}\r\n"
        response += "Content-Type: text/xml\r\n"
        response += f"Content-Length: {len(response_message)}\r\n"
        response += "\r\n"
        response += response_message

        client_socket.sendall(response.encode('utf-8'))
    finally:
        client_socket.close()

def run_server(host='0.0.0.0', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Middleware ejecutándose en http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_request, args=(client_socket, client_address)).start()

if __name__ == '__main__':
    run_server()