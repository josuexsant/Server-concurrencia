import unittest
import logging
from client import Client

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class TestClient(unittest.TestCase):

    def test_request_no(self):
        client = Client(r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\full')
        client.print_response()
        self.assertTrue(True)

    def test_request_empty(self):
        client = Client(r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\empty')
        client.print_response()
        self.assertTrue(True)

    def test_request_nonexistent(self):
        client = Client(r'C:\Users\josue\Desktop\Uni\Primavera2025\ServiciosWeb\propuesta\arqui\nonexistent')
        client.print_response()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
