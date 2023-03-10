from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QStyleFactory, QWidget, QVBoxLayout
import os
import socket
import lz4.frame
import pygame
from screeninfo import get_monitors
from socket import error as socket_error
import traceback
import logging


class DesktopViewer:
    ip_address = ""
    port = 0
    width = 0
    height = 0

    def __init__(self, ip_address, port, width, height):
        self.ip_address = ip_address
        self.port = int(port)
        self.width = int(width)
        self.height = int(height)
        self.main()

    def recvall(self, conn, length):
        """ Retrieve all pixels. """

        buf = b''
        while len(buf) < length:
            data = conn.recv(length - len(buf))
            if not data:
                return data
            buf += data
        return buf

    def main(self):
        pygame.init()

        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        clock = pygame.time.Clock()
        watching = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.ip_address, self.port))
                sock.sendall("remote_desktop".encode())
                while watching:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            watching = False
                            pygame.quit()
                            break
                    if watching == False:
                        sock.close()
                        break
                    # Retreive the size of the pixels length, the pixels length and pixels
                    size_len = int.from_bytes(sock.recv(1), byteorder='big')
                    size = int.from_bytes(sock.recv(size_len), byteorder='big')
                    # pixels = decompress(recvall(sock, size))
                    pixels = lz4.frame.decompress(self.recvall(sock, size))

                    # Create the Surface from raw pixels
                    img = pygame.image.fromstring(pixels, (self.width, self.height), 'RGB')

                    # RESIZE WINDOW (not working well)
                    """ext = img.get_rect()[2:4]
                    size = 0.9
        
                    image = pygame.transform.scale(
                        img,
                        (int(ext[0] * size), int(ext[1] * size))
                    )"""

                    # TRY LATER
                    # image = pygame.image.frombytes(pixels, (WIDTH, HEIGHT), 'RGB')

                    # image = pygame.transform.smoothscale(img, (WIDTH / 2, WIDTH / 2))

                    # Display the picture
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    clock.tick(120)
            except Exception as e:
                logging.error(traceback.format_exc())
            finally:
                sock.close()
