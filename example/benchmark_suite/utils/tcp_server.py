import argparse, socket
from time import sleep

ADDRESS = '0.0.0.0'
PORT = 4243

def recvall(sock):
    response = ''
    while True:
        more = sock.recv(1)
        if more:
            response += more.decode()
            if response[-1] == '\n':
                return response[:-1]
        else:
            return response

def send_bytes(sc, n):
    # data = 'a'
    # data *= n
    # data += '\n'
    # data = data.encode()
    sc.sendall(bytes(n) + '\n'.encode())

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    sc = sock.accept()[0]

    while True:
        data = recvall(sc)
        if not data:
            break
        bytes_to_send = int(data.strip())
        send_bytes(sc, bytes_to_send)

    sc.close()

server(ADDRESS,PORT)
