import string
from word_list import words_prob

def get_letters_frequency(word_list, game_state):
    letters_freq = {}
    for word in word_list:
        masked = game_state.get_masked(word)
        for index, letter in enumerate(masked):
            if letter not in letters_freq:
                letters_freq[letter] = { 'single': 0, 'double': 0, 'triple': 0, 'quad': 0, 'pent': 0 }
            if masked[:index].count(letter) == 0:
                letters_freq[letter]['single'] += 1
            if masked[:index].count(letter) == 1:
                letters_freq[letter]['double'] += 1
            if masked[:index].count(letter) == 2:
                letters_freq[letter]['triple'] += 1
            if masked[:index].count(letter) == 3:
                letters_freq[letter]['quad'] += 1
            if masked[:index].count(letter) == 4:
                letters_freq[letter]['quad'] += 1

    return letters_freq

def score_word(word, letters_freq, game_state):
    masked = game_state.get_masked(word)
    score = 0
    for index, letter in enumerate(masked):
        if masked[:index].count(letter) == 0:
            score += letters_freq[letter]['single']
        if masked[:index].count(letter) == 1:
            score += letters_freq[letter]['double']
        if masked[:index].count(letter) == 2:
            score += letters_freq[letter]['triple']
        if masked[:index].count(letter) == 3:
            score += letters_freq[letter]['quad']
        if masked[:index].count(letter) == 4:
            score += letters_freq[letter]['pent']
    
    return score

def make_guess(game_state):
    filtered_words = game_state.get_available_guesses()
    letters_freq =  get_letters_frequency(filtered_words, game_state)
    word_scores = {}
    for word in filtered_words:
        word_scores[word] = score_word(word, letters_freq, game_state)
    
    best_guess = None
    for word, score in word_scores.items():
        if best_guess is None: best_guess = word
        if word_scores[best_guess] < score:
            best_guess = word
        if word_scores[best_guess] == score:
            if word not in words_prob: continue
            if best_guess not in words_prob or words_prob[best_guess] < words_prob[word]:
                best_guess = word

    return best_guess

