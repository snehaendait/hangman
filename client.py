import socket

import connection

TCP_IP = '127.0.0.1'
TCP_PORT = 80
BUFFER_SIZE = 1024

WAITING_FOR_WELCOME = 0
WAITING_FOR_BOARD = 1
WAITING_FOR_GAME_STATUS = 2
WAITING_FOR_USER_INPUT = 3
WAITING_TO_PLAY_AGAIN = 4
GAME_OVER = 5

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((TCP_IP, TCP_PORT))
    #data = s.recv(BUFFER_SIZE)
    #print("received data:", data)
    return s

def quit(messenger):
    state = GAME_OVER
    messenger.send("quit")
    print ("Thanks for playing!")
    return state

if __name__ == "__main__":
    sock = create_socket()
    sock.connect((TCP_IP,TCP_PORT))
    messenger = connection.Connection(sock)
    current_state = WAITING_FOR_WELCOME

    while current_state is not GAME_OVER:
        if current_state is WAITING_FOR_WELCOME:
            print (messenger.read())
            current_state = WAITING_FOR_BOARD
        elif current_state is WAITING_FOR_BOARD:
            print (messenger.read())
            current_state = WAITING_FOR_GAME_STATUS
        elif current_state is WAITING_FOR_GAME_STATUS:
            msg = (messenger.read())
            if msg == "True":
                current_state = WAITING_TO_PLAY_AGAIN
            elif msg == "False":
                current_state = WAITING_FOR_USER_INPUT
        elif current_state is WAITING_FOR_USER_INPUT:
            guess = input("Guess a letter: ").lower()
            if guess == ":q":
                current_state = quit(messenger)
            elif len(guess) > 1 or not guess.isalpha():
                print ("Please guess a letter.")
            else:
                messenger.send(guess)
                current_state = WAITING_FOR_BOARD
        elif current_state is WAITING_TO_PLAY_AGAIN:
            play_again = input("Play again? (y/n): ").lower()
            if "y" in play_again:
                current_state = WAITING_FOR_WELCOME
                messenger.send("play")
            else:
                current_state = GAME_OVER
                messenger.send("quit")
                print ("Thanks for playing!")

    sock.close()
