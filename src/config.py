# config.py

#paths
TRAINING_FILE = "../input/testset_C.csv"
MODEL_OUTPUT = "../models/"

#Dataset
TEST_SIZE = 0.33
RANDOM_STATE = 42

#Hyperparameters
## TfIdf
sublinear_tf = True
min_df = 5
norm = 'l2'
encoding = 'latin-1' 
ngram_range = (1, 2)
stop_words = 'english'