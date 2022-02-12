import string
alphabet = list(string.ascii_lowercase)
from word_list import common_words, weird_words

class GameState:
    def __init__(self):
        self.score = 0
        self.template = ['', '', '', '', '']
        self.ruled_out_letters = set()
        self.letter_hints = {}
        for letter in alphabet:
            self.letter_hints[letter] = { 'hints': None, 'archived': None }

    def matches_template(self, word):
        for index, letter in enumerate(self.template):
            if letter == '': continue
            if letter != word[index]: return False
        return True

    # returns a list of characters from the word, after removing the letters from the template
    def get_masked(self, word):
        # this method relies on the word being passed to match the template
        if not self.matches_template(word): raise Exception
        return [word[index] for index in [0, 1, 2, 3, 4] if self.template[index] == '']

    def contains_ruled_out_letters(self, word):
        ruled_out_letters = [l for l in self.get_masked(word) if l in self.ruled_out_letters]
        return True if len(ruled_out_letters) else False

    def is_word_allowed(self, word):
        # if the word doesn't follow the template (green letters), it's ruled out
        if not self.matches_template(word): return False
        # if the word contains any ruled out letters, we can filter the word out
        if self.contains_ruled_out_letters(word): return False

        for letter, hints in self.letter_hints.items():
            # if we don't have any hints for the letter, we can't use it to filter out words
            if hints['hints'] is None: continue
            # the hints are a set of indices, and the word should have the letter at at least one of those
            if len([True for index in hints['hints'] if word[index] == letter]) == 0:
                return False
            # if the word has the letter at a position the hints doesn't, then it's ruled out
            if len([True for index in [0, 1, 2, 3, 4] if word[index] == letter and index not in hints['hints'] and self.template[index] != letter]) > 0:
                return False
        
        return True

    def get_available_guesses(self):
        # print(len([w for w in common_words if self.is_word_allowed(w)]))
        return [w for w in common_words if self.is_word_allowed(w)]

    def update(self, guess, results):
        self.score += 1
        for index, color in enumerate(results):
            letter = guess[index]
            if color == 'green':
                self.template[index] = letter
                if self.letter_hints[letter]['hints'] is not None:
                    self.letter_hints[letter]['archived'] = [i for i in self.letter_hints[letter]['hints'] if self.template[i] == '']
                    self.letter_hints[letter]['hints'] = None
        for index, color in enumerate(results):
            letter = guess[index]
            if color == 'yellow':
                letter = guess[index]
                if self.letter_hints[letter]['hints'] is None:
                    if self.letter_hints[letter]['archived'] is None:
                        self.letter_hints[letter]['hints'] = [i for i in [0, 1, 2, 3, 4] if i != index]
                    else:
                        self.letter_hints[letter]['hints'] = [i for i in self.letter_hints[letter]['archived'] if i != index]
                        self.letter_hints[letter]['archived'] = None
                else:
                    self.letter_hints[letter]['hints'] = [i for i in self.letter_hints[letter]['hints'] if i != index]
        for index, color in enumerate(results): 
            letter = guess[index]
            if color == 'white':
                if self.letter_hints[letter]['hints'] is None:
                    self.ruled_out_letters.add(letter)
                else:
                    self.letter_hints[letter]['hints'] = [i for i in self.letter_hints[letter]['hints'] if i != index]
