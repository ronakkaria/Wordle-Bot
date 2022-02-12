import csv
import os

words = []
words_freq = {}
total_freq_count = 0

common_words = []
weird_words = []

with open(os.path.dirname(__file__) + '/five_letter_unigram_freq.csv', 'r') as word_list_file:
    reader = csv.DictReader(word_list_file)
    for row in reader:
        words.append(row['word'])
        words_freq[row['word']] = int(row['count'])
        total_freq_count += int(row['count'])


words_prob = {}

for word in words:
    words_prob[word] = words_freq[word] / total_freq_count

with open(os.path.dirname(__file__) + '/wordle_normal_words.csv', 'r') as wordle_normal_file:
    reader = csv.reader(wordle_normal_file)
    for row in reader:
        common_words.append(row[0])

with open(os.path.dirname(__file__) + '/wordle_weird_words.csv', 'r') as wordle_weird_file:
    reader = csv.reader(wordle_weird_file)
    for row in reader:
        weird_words.append(row[0])
