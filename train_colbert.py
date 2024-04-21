# # git -C ColBERT/ pull || git clone https://github.com/stanford-futuredata/ColBERT.git
import sys; sys.path.insert(0, 'ColBERT/')

from colbert import Trainer
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection
import csv
import random
random.seed(42)
import json
from sentence_transformers import CrossEncoder
import yake
import numpy as np
import os
import re

all_genres = set()
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
keyword_extractor = yake.KeywordExtractor(top=5, n=1)

def extract_keywords(text):
    # Extract keywords from the text
    keywords = keyword_extractor.extract_keywords(text)

    # Get only the keywords from the extracted tuples and concatenate into a single string
    keywords_list = [keyword[0] for keyword in keywords]
    keywords_string = ' '.join(keywords_list)

    return keywords_string

def get_genre_to_lyrics(tsv_file):
    genre_to_lyrics = {}
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            genre, lyrics = line
            if genre not in genre_to_lyrics:
                genre_to_lyrics[genre] = []
                all_genres.add(genre)
            genre_to_lyrics[genre].append(lyrics)
    return genre_to_lyrics

def read_tsv(tsv_file):
    collection = []
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 2:
                continue
            collection.append(row[1])

    return collection

def write_queries_tsv(triple_tsv_file, id_to_song, tsv_file):
    with open(triple_tsv_file, 'r') as tf, open(tsv_file, 'w') as qf:
        lines = tf.readlines()
        for line in lines:
            row = re.findall(r'\d+', line)
            q_id, positive_id, negative_id = row
            positive_song = id_to_song[int(positive_id)]
            negative_song = id_to_song[int(negative_id)]

            pairs = [(extract_keywords(positive_song), negative_song) for i in range(4)]
            query = get_worst_sample(pairs)[0]

            text = f"{q_id}\t{query}\n"
            qf.write(text)
               
def write_triples_tsv(genre_to_lyrics, tsv_file, song_to_id):
    with open(tsv_file, 'w') as f:
        q_id = 0
        sorted_genre_to_lyrics = dict(sorted(genre_to_lyrics.items()))
        for genre, songs in sorted_genre_to_lyrics.items():
            for song in songs:
                positive_id = song_to_id[song]
                negative_id = get_negative_sample(song, genre, genre_to_lyrics, song_to_id)
                triple = f'[{q_id}, {positive_id}, {negative_id}]\n'
                f.write(triple)
                q_id += 1

def get_worst_sample(pairs):
    scores = model.predict(pairs)
    return pairs[np.argmin(scores)]

def get_negative_sample(positive_song, positive_genre, genre_to_lyrics, song_to_id):
    pairs = []
    for i in range(4):
        random_negative_genre = random.choice([g for g in all_genres if g != positive_genre])
        negative_song = random.choice(genre_to_lyrics[random_negative_genre])
        pairs.append((positive_song, negative_song))

    return song_to_id[get_worst_sample(pairs)[1]]

if __name__=='__main__':
    triples_path = 'triples.tsv'
    queries_path = 'queries.tsv'
    collection_genre_path = 'combined_with_genre.tsv'
    collection_path = 'combined_without_genre.tsv'

    if not os.path.exists(triples_path) or not os.path.exists(queries_path):
        collection_lst = read_tsv(collection_genre_path)
        song_to_id = {song: idx for idx, song in enumerate(collection_lst)}
        id_to_song = {idx: song for idx, song in enumerate(collection_lst)}
        genre_to_lyrics = get_genre_to_lyrics(collection_genre_path)

        write_triples_tsv(genre_to_lyrics, triples_path, song_to_id)
        write_queries_tsv(triples_path, id_to_song, queries_path)

    experiment_name = 'trained_my_lyrics_experiment'
    print('training')
    with Run().context(RunConfig(nranks=1, experiment=experiment_name)):
        config = ColBERTConfig(
            bsize=32,
            root="./experiments",
        )
        trainer = Trainer(
            triples=triples_path,
            queries=queries_path,
            collection=collection_path,
            config=config,
        )

        checkpoint_path = trainer.train()

        print(f"Saved checkpoint to {checkpoint_path}...")
