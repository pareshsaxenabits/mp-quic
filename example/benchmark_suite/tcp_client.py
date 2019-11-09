import argparse, socket
from time import sleep, time

ADDRESS = '100.0.0.1'
PORT = 4243
BLOCK_SIZE = 1024       # bytes
ON_OFF_INTERVAL = 0.002 # seconds
ITERATIONS = 10

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

def client(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    for i in range(ITERATIONS):
        message = str(BLOCK_SIZE) + '\n'

        sock.sendall(message.encode())
        recvall(sock)

        sleep(ON_OFF_INTERVAL)

    sock.close()

start = time()
client(ADDRESS,PORT)
end = time()
time_taken = end - start

print(int(time_taken * 1e9),end='')
