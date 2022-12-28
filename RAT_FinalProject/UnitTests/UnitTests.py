import unittest
import socket


def return_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipaddress = s.getsockname()[0]
    s.close()
    return ipaddress


class TestIpAddress(unittest.TestCase):
    def test_return_ip_address(self):
        # Test that the function returns a string
        self.assertIsInstance(return_ip_address(), str)

        # Test that the returned string is a valid IP address
        self.assertRegex(return_ip_address(), r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')


if __name__ == '__main__':
    unittest.main()


