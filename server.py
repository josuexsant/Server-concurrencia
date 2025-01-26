from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os

def search_dir(directory_path):
    import os
    if os.path.isdir(directory_path):
        try:
            # Listar el contenido del directorio
            contents = os.listdir(directory_path)
            return {'status': 200, 'contents': contents if contents else "El directorio está vacío"}
        except Exception as e:
            return {'status': 500, 'message': f"Error al listar el contenido del directorio: {e}"}
    else:
        return {'status': 404, 'message': "El directorio no existe"}

with SimpleXMLRPCServer(('127.0.0.1', 8000), requestHandler=SimpleXMLRPCRequestHandler) as server:
    server.register_function(search_dir, 'searchDir')
    print('Servidor en ejecución en el puerto 8000...')
    server.serve_forever()
