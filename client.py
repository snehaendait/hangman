import socket

import connection

TCP_IP = '127.0.0.1'  # localhost
TCP_PORT = 5000
BUFFER_SIZE = 1024

WAITING_FOR_SERVER_CONNECTION = 0
WAITING_FOR_GAME = 1
WAITING_FOR_RESULT = 2
WAITING_FOR_USER_INPUT = 3
WAITING_TO_PLAY_AGAIN = 4
GAME_END = 5


def create_socket():  # create a simple TCP-IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s


def quit(messenger):  # function to quit game
    state = GAME_END  # set the game state to end
    messenger.send("quit")
    print("Thanks for playing!")
    return state

if __name__ == "__main__":
    sock = create_socket()
    sock.connect((TCP_IP,TCP_PORT))
    connector = connection.Connection(sock)
    current_state = WAITING_FOR_SERVER_CONNECTION

    while current_state is not GAME_END:  # keep playing until the game is not ended
        if current_state is WAITING_FOR_SERVER_CONNECTION:
            print (connector.read())
            current_state = WAITING_FOR_GAME
        elif current_state is WAITING_FOR_GAME:  # check if the game is still in progress
            print (connector.read())
            current_state = WAITING_FOR_RESULT
        elif current_state is WAITING_FOR_RESULT:
            msg = (connector.read())
            if msg == "True":
                current_state = WAITING_TO_PLAY_AGAIN
            elif msg == "False":
                current_state = WAITING_FOR_USER_INPUT
        elif current_state is WAITING_FOR_USER_INPUT:  # check the user input
            guess = input("Guess a letter: ").lower()
            if guess == ":q":  # allows the user to quit using :q
                current_state = quit(connector)
            elif len(guess) > 1 or not guess.isalpha():  # else check if the input is not valid
                print ("Please guess a letter.")
            else:  # if the input is valid send it to the server to guess
                connector.send(guess)
                current_state = WAITING_FOR_GAME
        elif current_state is WAITING_TO_PLAY_AGAIN:  # check if the user wants to play again
            play_again = input("Play again? (y/n): ").lower()
            if "y" in play_again:
                current_state = WAITING_FOR_SERVER_CONNECTION
                connector.send("play")
            else:
                current_state = GAME_END
                connector.send("quit")
                print ("Thanks for playing!")

    sock.close()
