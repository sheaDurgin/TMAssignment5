# git -C ColBERT/ pull || git clone https://github.com/stanford-futuredata/ColBERT.git
import sys; sys.path.insert(0, 'ColBERT/')

from colbert import Searcher
import csv
import yake

keyword_extractor = yake.KeywordExtractor(top=5, n=1)

def extract_keywords(text):
    # Extract keywords from the text
    keywords = keyword_extractor.extract_keywords(text)

    # Get only the keywords from the extracted tuples and concatenate into a single string
    keywords_list = [keyword[0] for keyword in keywords]
    keywords_string = ' '.join(keywords_list)

    return keywords_string

def read_tsv(tsv_file):
    collection = []
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            collection.append(row[1])

    return collection

if __name__ == '__main__':    
    collection = read_tsv('combined.tsv')

    index_name = 'my_lyrics_index/'
    searcher = Searcher(index=index_name, collection=collection)

    queries = read_tsv('test.tsv')

    with open('search_results.tsv', 'w') as f:
        # using passage id in place of title, no title in data from previous assignment
        f.write("query\tQ0\tpassage_id\trank\tscore\ttag\n")
        for query in queries:
            # Perform the search
            results = searcher.search(query, k=10)
            query = extract_keywords(query)
            for p_id, rank, score in zip(*results):
                f.write(f"{query}\tQ0\t{p_id}\t{rank}\t{score:.1f}\tSheaD\n")