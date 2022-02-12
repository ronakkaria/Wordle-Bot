import csv
import os

with open(os.path.dirname(__file__) + '/unigram_freq.csv', mode='r') as full_word_list_file:
    with open(os.path.dirname(__file__) + '/five_letter_unigram_freq.csv', mode='w') as five_letter_word_list_file:
        reader = csv.DictReader(full_word_list_file)
        writer = csv.DictWriter(five_letter_word_list_file, ['word', 'count'])
        writer.writeheader()
        for row in reader:
            if len(row['word']) != 5: continue
            writer.writerow(row)
