Shea Durgin

# necessary installs  
DOES NOT WORK ON WINDOWS, USE MAC OR LINUX  
run `python -m venv myvenv` or `python3 -m venv myvenv`  
run `source myvenv/bin/activate` 

run `git clone https://github.com/stanford-futuredata/ColBERT.git`
run `git -C ColBERT/ pull`
run `pip install -r requirements.txt` or `pip3 install -r requirements.txt` 

# info
all combined*.tsv files were created with train.tsv and validation.tsv  
if these tsvs are needed for any reason, they are in my assignment4 submission  

# task 1
run `python index_colbert.py`  
this indexes all documents, and can now be searched on
run `python search_colbert.py`  
searched the previously created index  
queries are just a concatenation of generated keywords from songs in the test.tsv  
using passage id in place of title, no title in data from previous assignment  
craetes a saerch_results.tsv, `query	Q0	passage_id	rank	score	tag`

# task 2
run `python train_colbert.py`
trains a colbert model and saves in the previously made experiments folder  
triples.tsv and queries.tsv are generated in train_colbert.py, if either one is missing  
triples.tsv is a JSONL type file in this format, `[qid, pid+, pid-]`  
`+`: positive sample  
`-`: negative sample  
queries.tsv is a tsv in this format, `qid, query`
