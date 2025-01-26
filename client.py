import socket

class Client:
    middleware_port = 8080
    middleware_ip = '127.0.0.1'
    
    def __init__(self, path):
        self.path = path
        response = self.request()
        
    def request(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.middleware_ip, self.middleware_port))
            client_socket.sendall(self.path.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            return response
        
    def print_response(self):
        print("-" * 50)
        print(self.request())
        print("-" * 50)
        
