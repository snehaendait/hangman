EOM = "~"


class Connection:
    def __init__(self, sock):
        self.data = ""
        self.sock = sock

    def read(self):
        if not EOM in self.data:
            self.data += self.sock.recv(1024).decode('utf-8')

        msg, self.data = self.data.split(EOM, 1)
        return msg

    def send(self, msg):
        self.sock.sendall((msg + EOM).encode('utf-8'))
