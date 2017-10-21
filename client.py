import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 80
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode('utf-8'))
    data = s.recv(BUFFER_SIZE)
    print("received data:", data)
    return s

if __name__ == "__main__":
    sock = create_socket()
    sock.close()
