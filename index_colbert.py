# git -C ColBERT/ pull || git clone https://github.com/stanford-futuredata/ColBERT.git
import sys; sys.path.insert(0, 'ColBERT/')

from colbert import Indexer, Searcher
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection
import csv

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
    model_path = 'colbert-ir/colbertv2.0'

    # Path to your TSV file containing genre names mapping to lyrics
    collection = read_tsv('combined.tsv')

    index_name = 'my_lyrics_index'
    experiment_name = 'my_lyrics_experiment'

    # Initialize the Indexer
    with Run().context(RunConfig(nranks=1, experiment=experiment_name)):
        config = ColBERTConfig(
            nbits=2,
            root='./experiments'
        )
        indexer = Indexer(checkpoint=model_path, config=config)
        indexer.index(name=index_name, collection=collection, overwrite=True)

        print(indexer.get_index())

