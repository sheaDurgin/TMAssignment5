import csv
import random
random.seed(42)

def get_genre_to_lyrics(tsv_file, genre_to_lyrics={}):
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for line in reader:
            genre, lyrics = line
            if genre not in genre_to_lyrics:
                genre_to_lyrics[genre] = []
            genre_to_lyrics[genre].append(lyrics)
    return genre_to_lyrics

def remove_first_column(output_file, genre_to_lyrics):
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        idx = 0
        sorted_genre_to_lyrics = dict(sorted(genre_to_lyrics.items()))
        for genre, songs in sorted_genre_to_lyrics.items():
            for song in songs:
                writer.writerow([idx, song])
                idx += 1

def combine_some(output_file, genre_to_lyrics):
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        sorted_genre_to_lyrics = dict(sorted(genre_to_lyrics.items()))
        for genre, songs in sorted_genre_to_lyrics.items():
            for song in songs[:100]:
                writer.writerow([genre, song])

def combine(output_file, genre_to_lyrics):
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        sorted_genre_to_lyrics = dict(sorted(genre_to_lyrics.items()))
        for genre, songs in sorted_genre_to_lyrics.items():
            for song in songs:
                writer.writerow([genre, song])


# Example usage:
input_file1 = 'train.tsv'
input_file2 = 'validation.tsv'

genre_to_lyrics = get_genre_to_lyrics(input_file1)
genre_to_lyrics = get_genre_to_lyrics(input_file2, genre_to_lyrics)

output_file1 = 'combined_with_genre.tsv'
output_file2 = 'combined_without_genre.tsv'
combine_some(output_file1, genre_to_lyrics)

remove_first_column(output_file2, genre_to_lyrics)

output_file3 = 'combined.tsv'
combine(output_file3, genre_to_lyrics)
