import socket
import time
import xmlrpc.client
import threading

def middleware(request, client_address):
    request_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("=" * 50)
    print(request_time + f" : Request from {client_address[0]}")
    print(f"Path requested: {request}")

    # Conexión con el servidor XML-RPC local
    server_ip = '127.0.0.1'  # Servidor está en la misma máquina
    server_port = 8000       # Puerto del servidor XML-RPC
    proxy = xmlrpc.client.ServerProxy(f'http://{server_ip}:{server_port}')
    response = proxy.searchDir(request)
    print(f"Response: {response}")
    if response['status'] == 404:
        return response['status'], response['message']
    return response['status'], response.get('contents', '')

def handle_request(client_socket, client_address):
    """Maneja la solicitud del cliente."""
    try:
        # Recibir los datos de la solicitud
        request = client_socket.recv(1024).decode('utf-8')

        # Procesar la solicitud mediante el middleware
        status_code, response_message = middleware(request, client_address)

        # Convertir la respuesta a un string si es una lista
        if isinstance(response_message, list):
            response_message = "\n".join(response_message)  # Une los elementos de la lista en un string

        # Convertir la respuesta a un string si es un diccionario
        if isinstance(response_message, dict):
            response_message = str(response_message)

        # Formatear la respuesta con el código de estado
        response = f"HTTP/1.1 {status_code} {'OK' if status_code == 200 else 'Not Found'}\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: {}\r\n".format(len(response_message))
        response += "\r\n"
        response += response_message

        # Respuesta al cliente
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
