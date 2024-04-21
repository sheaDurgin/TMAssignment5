necessary installs
run `git -C ColBERT/ pull || git clone https://github.com/stanford-futuredata/ColBERT.git`
run `pip install -r requirements.txt`

scripts to run for assignment  

index_colbert.py  
search_colbert.py  
train_colbert.py  

get_combined.py was used to generate the combined files, no need to run again.  
train and validation are used in get_combined.py  
test is used in search_colbert.py  
trples and queries are generated in train_colbert.py