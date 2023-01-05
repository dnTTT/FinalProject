import unittest
import socket
import ssl

HOST = '192.168.1.173'
PORT = 65432

class TestServer(unittest.TestCase):
    def test_server_starts(self):
        # Test that the server starts and binds to the correct host and port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            self.assertEqual(sock.getsockname(), (HOST, PORT))

    def test_client_connection(self):
        # Test that the server can accept a client connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            sock.listen(5)

            client_sock, client_address = sock.accept()
            self.assertIsInstance(client_sock, socket.socket)
            self.assertEqual(client_address, ('192.168.1.173', 65432))

    def test_ssl_connection(self):
        # Test that the server can establish an SSL connection with a client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            sock.listen(5)

            client_sock, client_address = sock.accept()
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="mycert.pem")
            context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
            context.set_ciphers('AES256+ECDH:AES256+EDH')
            ssl_client_sock = context.wrap_socket(client_sock, server_side=True)

            self.assertIsInstance(ssl_client_sock, ssl.SSLSocket)

    def test_data_reception(self):
        # Test that the server can receive data from the client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            sock.listen(5)

            client_sock, client_address = sock.accept()
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="mycert.pem")
            context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
            context.set_ciphers('AES256+ECDH:AES256+EDH')
            ssl_client_sock = context.wrap_socket(client_sock, server_side=True)

            data = ssl_client_sock.recv(1024)
            self.assertGreater(len(data), 0)

    def test_data_decoding(self):
        # Test that the server can decode the data received from the client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            sock.listen(5)

            client_sock, client_address = sock.accept()
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="mycert.pem")
            context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
            context.set_ciphers('AES256+ECDH:AES256+EDH')
            ssl_client_sock = context.wrap_socket(client_sock, server_side=True)

            data = ssl_client_sock.recv(1024)
            ip_address, running_port, mac_address, width, height = data.decode("Utf-8").split("||")
            self.assertIsInstance(ip_address, str)
            self.assertIsInstance(running_port, str)
            self.assertIsInstance(mac_address, str)
            self.assertIsInstance(width, str)
            self.assertIsInstance(height, str)

    if __name__ == '__main__':
        unittest.main()