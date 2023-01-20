import pandas as pd
import random

data = pd.read_csv("./Deep-Learning-for-processing-of-literary-text/ge-en-mapping.csv",sep=";")
de_title = data["german-title"].to_list()
random.Random(123).shuffle(de_title)

train_de = de_title[:27]
valid_de = de_title[27:31]
test_de = de_title[31:]

train_en = [data["english-title"].loc[data["german-title"] == title] for title in train_de]
# train_set = pd.concat(train_set,axis=0)

valid_en = [data["english-title"].loc[data["german-title"] == title] for title in valid_de]
# valid_set = pd.concat(valid_set,axis=0)

test_en = [data["english-title"].loc[data["german-title"] == title] for title in test_de]
# test_set = pd.concat(test_set,axis=0)
