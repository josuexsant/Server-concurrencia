import unittest
import logging
from client import Client
import random

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class TestClient(unittest.TestCase):

  def setUp(self):
    logger.info(f'\n{"="*20}\nIniciando prueba: {self._testMethodName}\n{"="*50}')

  def test_request(self):
    client = Client(r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\full')
    response = client.request()
    client.print_response()
    expected_response = 'HTTP/1.1 200 OK'
    logger.info(f'Respuesta esperada: {expected_response}')
    logger.info(f'Respuesta recibida: {response}')
    self.assertTrue(response.startswith(expected_response))
    logger.info('Test de directorio lleno aprobado')

  def test_request_nonexistent_directory(self):
    client = Client(r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\nonexistent')
    response = client.request()
    client.print_response()
    expected_response = 'HTTP/1.1 404 Not Found'
    logger.info(f'Respuesta esperada: {expected_response}')
    logger.info(f'Respuesta recibida: {response}')
    self.assertTrue(response.startswith(expected_response))
    logger.info('Test de directorio no existente aprobado')

  def test_request_empty_directory(self):
    client = Client(r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\empty')
    response = client.request()
    client.print_response()
    expected_response = 'HTTP/1.1 200 OK'
    logger.info(f'Respuesta esperada: {expected_response}')
    logger.info(f'Respuesta recibida: {response}')
    self.assertTrue(response.startswith(expected_response))
    logger.info('Test de directorio vacio aprobado')
    
  def test_multiple_requests(self):
    directories = [
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\full',
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\nonexistent',
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\empty'
    ]
    expected_responses = [
      'HTTP/1.1 200 OK',
      'HTTP/1.1 404 Not Found',
      'HTTP/1.1 200 OK'
    ]
    
    for i, directory in enumerate(directories):
      client = Client(directory)
      response = client.request()
      expected_response = expected_responses[i]
      logger.info(f'Petición {i+1}: Respuesta esperada: {expected_response}')
      logger.info(f'Petición {i+1}: Respuesta recibida: {response}')
      self.assertTrue(response.startswith(expected_response))
    logger.info('Test de múltiples peticiones aprobado')
    
  def test_random_requests(self):
    directories = [
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\full',
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\nonexistent',
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\empty'
    ]
    expected_responses = {
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\full': 'HTTP/1.1 200 OK',
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\nonexistent': 'HTTP/1.1 404 Not Found',
      r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\empty': 'HTTP/1.1 200 OK'
    }
    
    for i in range(1000):
      directory = random.choice(directories)
      client = Client(directory)
      response = client.request()
      expected_response = expected_responses[directory]
      logger.info(f'Petición {i+1}: Respuesta esperada: {expected_response}')
      logger.info(f'Petición {i+1}: Respuesta recibida: {response}')
      self.assertTrue(response.startswith(expected_response))
    logger.info('Test de 1000 peticiones aleatorias aprobado')

if __name__ == '__main__':
  unittest.main()
