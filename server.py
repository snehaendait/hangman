import socket
from hangman import hangman
from threading import Thread
import connection

WAITING_FOR_CLIENT = 1
WAITING_FOR_INPUT = 2
WAITING_TO_PLAY_AGAIN = 3
WAITING_TO_START_GAME = 4
GAME_END = 5

class ClientThread(Thread):
    """
    class client thread will utilize a thread for every client connection
    so that all clients can be executed on different threads
    """
    def __init__(self, ip, port, socket):  # Initialize client thread with client's ip, port and socket
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.games_won = 0
        self.games_lost = 0
        print("[+] New game started for "+ip+":"+str(port))

    def run(self):  # Logic to run the game using multiple states
        current_state = WAITING_TO_START_GAME
        connector = connection.Connection(self.socket)
        while current_state is not GAME_END:  # Keep playing until the user wants to end the game
            if current_state is WAITING_TO_START_GAME:
                game = inititialize_game(connector)  # send welcome note to client
                current_state = WAITING_FOR_INPUT  # ask for user to input a letter (or quit command :q)
            elif current_state is WAITING_FOR_INPUT:
                letter = connector.read()  # get user input
                if letter == "quit":  # allows user to quit a current game using :q
                    current_state = GAME_END
                    reply = ""
                elif letter in game.right or letter in game.wrong:  # check if the input has already been attempted
                    reply = "You already tried %r! Try again " % letter
                else:
                    game.guess(letter)
                    reply = str(game)

                if game.end:  # if the game got over, ask if user wants to play it again
                    if game.won:
                        self.games_won = self.games_won + 1
                    else:
                        self.games_lost = self.games_lost + 1
                    reply += "\nNumber of games won: %s" % self.games_won
                    reply += "\nNumber of games lost: %s" % self.games_lost
                    current_state = WAITING_TO_PLAY_AGAIN
                connector.send(reply)
                connector.send(str(game.end))
            elif current_state is WAITING_TO_PLAY_AGAIN:
                play_again = connector.read()
                if play_again == "play":
                    current_state = WAITING_TO_START_GAME
                elif play_again == "quit":
                    current_state = GAME_END

        self.socket.close()

def inititialize_game(connection):
        game = hangman()
        connection.send("HELLO!! LET'S PLAY HANGMAN")
        connection.send(str(game))
        connection.send(str(game.end))
        return game


def create_socket():  # create a simple TCP-IP socket
    TCP_IP = '0.0.0.0'  # local IP - TODO: allow user to customize the host
    TCP_PORT = 5000

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    tcpsock.listen(4)
    return tcpsock


if __name__ == "__main__":
    sock = create_socket()
    threads = []
    while True:  # keep the server alive
        print("Waiting for incoming connections...")
        (conn, (ip, port)) = sock.accept()
        newthread = ClientThread(ip, port, conn)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()
