import csv
from termcolor import colored
from game_state import GameState
import algo_basic_letter_frequency
from word_list import common_words

first_guess = 'crate'

def play_game(answer):
    game_state = GameState()
    # print('\n')
    while ''.join(game_state.template) != answer:
        guess = algo_basic_letter_frequency.make_guess(game_state) if game_state.score > 0 else first_guess
        results = ['white', 'white', 'white', 'white', 'white']

        for index, letter in enumerate(guess):
            if letter in answer and answer[index] == letter:
                results[index] = 'green'

        masked_answer = [answer[index] for index in [0, 1, 2, 3, 4] if results[index] != 'green']

        for index, letter in enumerate(guess):
            if results[index] == 'green': continue
            if letter in masked_answer:
                results[index] = 'yellow'
                masked_answer.remove(letter)
    
        # print(*[colored(' ' + guess[i].upper() + ' ', 'white', 'on_' + results[i], attrs=['bold', 'concealed']) for i in [0, 1, 2, 3, 4]])
        # print('\n')
        print(*[colored(guess[i].upper(), results[i], attrs=['bold']) for i in [0, 1, 2, 3, 4]])
        game_state.update(guess, results)

    return game_state.score

answer = '' 
while (len(answer) != 5):
    answer = input('Enter the word\n')
play_game(answer)

# average_score = 0
# for i, word in enumerate(common_words):
#     # print(i+1, word, average_score / (i+1), end='\r')
#     average_score += play_game(word)
# print(colored(first_guess.upper(), 'cyan'), 'Average Score:', colored(round(average_score / len(common_words), 2), 'green'))

