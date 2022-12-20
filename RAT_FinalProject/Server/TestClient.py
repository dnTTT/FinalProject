import socket, ssl

HOST, PORT = '192.168.2.72', 65432


def handle(conn):
    #conn.write(b'GET / HTTP/1.1\n')
    conn.sendall(b'GET / HTTP/1.1')
    print(conn.recv().decode())


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

    conn = context.wrap_socket(sock, server_hostname=HOST)

    try:
        conn.connect((HOST, PORT))
        handle(conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
