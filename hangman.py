import random

class hangman:
    LIMIT = 10

    def __init__(self):  # initialize game
        self.word = self.get_random_word().lower()
        self.right = []
        self.wrong = []
        self.won = False
        self.end = False

    def get_random_word(self):  # get a random word from the word list - TODO: modify this to get words of animals, places, bases on user choices
        wordlist = open('wordlist.txt','r').readlines()
        words = [word.strip() for word in wordlist]
        return random.choice(words)

    def guess(self, letter):  # check if the guessed letter is correct
        if letter in self.word:
            self.right.append(letter)
        else:
            self.wrong.append(letter)

    def result(self):  # return the result of the game - won, lost, in progress
        if set(self.right) == set(self.word) and len(self.wrong) < self.LIMIT:
            result = "Won!"
            self.won = True
            self.end = True
        elif len(self.wrong) >= self.LIMIT:
            result = "Lost! The word was %r" % self.word
            self.end = True
        else:
            result = "Game in progress.. To quit, type ':q'"
        return result

    def show_correct_guesses(self):  # method to display progress
        return " ".join([letter if letter in self.right else "_" for letter in self.word])


    def __str__(self):
        result = "\n" + "#" * 30 + "\n"
        result += "\nIncorrect guesses: %s" % ", ".join(self.wrong)
        result += "\nProgress: %s" % self.show_correct_guesses()
        result += "\n" + self.result()
        return result

def get_guess(game):
    while True:
        guess = input("Guess a letter: ").lower()
        if len(guess) > 1 or not guess.isalpha() :
            print("Please input one character: ")
        elif guess in game.right or guess in game.wrong:
            print("You already tried that input! Try again: ")
        else:
            return guess

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
        keep_playing = input("Do you want to keep playing y/n? : ").lower()
        if keep_playing == 'n':
            play_more = False
