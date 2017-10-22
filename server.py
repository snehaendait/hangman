import socket
from hangman import hangman
from threading import Thread
import connection

WAITING_FOR_CONN = 1
WAITING_FOR_MOVE = 2
WAITING_TO_PLAY_AGAIN = 3
WAITING_TO_START_GAME = 4
GAME_OVER = 5

class ClientThread(Thread):

    def __init__(self, ip, port, socket):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        print("[+] New game started for "+ip+":"+str(port))


    def run(self):
        current_state = WAITING_TO_START_GAME
        messenger = connection.Connection(self.socket)
        while current_state is not GAME_OVER:
            if current_state is WAITING_TO_START_GAME:
                game = inititialize_game(messenger)
                current_state = WAITING_FOR_MOVE
            elif current_state is WAITING_FOR_MOVE:
                letter = messenger.read()
                if letter in game.right or letter in game.wrong:
                    reply = "You already tried %r! Try again " % letter
                else:
                    game.guess(letter)
                    reply = str(game)

                if game.end:
                    current_state = WAITING_TO_PLAY_AGAIN
                messenger.send(reply)
                messenger.send(str(game.end))
            elif current_state is WAITING_TO_PLAY_AGAIN:
                play_again = messenger.read()
                if play_again == "play":
                    current_state = WAITING_TO_START_GAME
                elif play_again == "quit":
                    current_state = GAME_OVER

        self.socket.close()

def inititialize_game(connection):
        game = hangman()
        connection.send("HELLO!! LET'S PLAY HANGMAN")
        connection.send(str(game))
        connection.send(str(game.end))
        return game

def create_socket():
    TCP_IP = '0.0.0.0'
    TCP_PORT = 80

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    tcpsock.listen(4)
    return tcpsock


if __name__ == "__main__":
    sock = create_socket()
    threads = []
    while True:
        print("Waiting for incoming connections...")
        (conn, (ip, port)) = sock.accept()
        newthread = ClientThread(ip, port, conn)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()
