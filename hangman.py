import random
import string

from awscli.compat import raw_input


class hangman:
    LIMIT = 10

    def __init__(self):
        self.word = self.get_random_word().lower()
        self.right = []
        self.wrong = []
        self.end = False

    def get_random_word(self):
        wordlist = open('wordlist.txt','r').readlines()
        words = [word.strip() for word in wordlist]
        return random.choice(words)

    def guess(self, letter):
        if letter in self.word:
            self.right.append(letter)
        else:
            self.wrong.append(letter)

    def result(self):
        if set(self.right) == set(self.word) and len(self.wrong) < self.LIMIT:
            result = "Won!"
            self.end = True
        elif len(self.wrong) >= self.LIMIT:
            result = "Lost!"
            self.end = True
        else:
            result = "Still in progress"
        return result

    def show_correct_guesses(self):
        return " ".join([letter if letter in self.right else "_" for letter in self.word])


def get_guess(game):
    while True:
        input = raw_input("Guess a letter: ").lower()
        if len(input) > 1 or not input.isalpha() :
            print("Please input one character: ")
        elif input in game.right or input in game.wrong:
            print("You already tried that input! Try again: ")
        else:
            return input

if __name__ == "__main__":
    play_more = True
    while play_more:
        game = hangman()
        print("HELLO!!! LETS PLAY HANGMAN")
        while not game.end:
            guess_letter = get_guess(game)
            game.guess(guess_letter)
            print(game.show_correct_guesses())
            game.result()
        print(game.result())
        print(game.word)
        keep_playing = raw_input("Do you want to keep playing y/n? : ").lower()
        if keep_playing == 'n':
            play_more = False
