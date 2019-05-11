from .exceptions import *
import random

class GuessAttempt(object):

    def __init__(self, guess, hit=False, miss=False):
        if hit and miss:
            raise InvalidGuessAttempt

        self.guess = guess
        self.hit = hit
        self.miss = miss

    def is_hit(self):
        return self.hit

    def is_miss(self):
        return self.miss

class GuessWord(object):

    def __init__(self, answer):
        if not answer:
            raise InvalidWordException
        self.answer = answer
        self.masked = "*" * len(self.answer)

    def perform_attempt(self, guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException
        attempt = GuessAttempt(guess, guess.lower() in self.answer.lower(),\
                                      guess.lower() not in self.answer.lower())
        self.masked = self.uncover_word(guess)
        return attempt

    def uncover_word(self, guess):
        new_masked = ''
        for i,c in enumerate(self.masked):
            if self.answer[i].lower() == guess.lower():
                new_masked += guess.lower()
            else:
                new_masked += self.masked[i]
        self.masked = new_masked
        return self.masked

class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, list_of_words=WORD_LIST, number_of_guesses=5):
        self.words = list_of_words
        self.word = GuessWord(self.select_random_word(self.words))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []

    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        return random.choice(list_of_words)

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException
        self.previous_guesses.append(letter.lower())
        self.word.uncover_word(letter)

        if letter.lower() not in self.word.answer.lower():
            self.remaining_misses -= 1

        if self.is_won():
            raise GameWonException
        if self.is_lost():
            raise GameLostException

        return GuessAttempt(letter, letter.lower() in self.word.answer.lower(),
                                    letter.lower() not in self.word.answer.lower())

    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.remaining_misses == 0

    def is_finished(self):
        return self.is_won() or self.is_lost()

#game = HangmanGame(['aaa'])
#game.guess('a')
#print(game.word.answer, game.word.masked)
