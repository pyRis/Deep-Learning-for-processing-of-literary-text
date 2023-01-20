import pandas as pd
import random
import shutil
import os

data = pd.read_csv("./Deep-Learning-for-processing-of-literary-text/ge-en-mapping.csv",sep=";")
de_title = data["german-title"].to_list()
random.Random(123).shuffle(de_title)

#get lists of german data split 
train_de = de_title[:27]
valid_de = de_title[27:31]
test_de = de_title[31:]

#get lists of english data split 
train_set = [data.loc[data["german-title"] == title] for title in train_de]
train_set = pd.concat(train_set,axis=0)
train_en = train_set["english-title"].to_list()

valid_set = [data.loc[data["german-title"] == title] for title in valid_de]
valid_set = pd.concat(valid_set,axis=0)
valid_en = valid_set["english-title"].to_list()

test_set = [data.loc[data["german-title"] == title] for title in test_de]
test_set = pd.concat(test_set,axis=0)
test_en = test_set["english-title"].to_list()

print(train_en,valid_en,test_en)
print(train_de,valid_de,test_de)

#remove “” in play name
train_en = [play.lstrip('“').rstrip('”') for play in train_en]
valid_en = [play.lstrip('“').rstrip('”') for play in valid_en]
test_en = [play.lstrip('“').rstrip('”') for play in test_en]


#get english split sets
for play in train_en:
    shutil.copyfile(os.path.join("./data/EN",play),os.path.join("./data/EN/train",play))
for play in valid_en:
    shutil.copyfile(os.path.join("./data/EN",play),os.path.join("./data/EN/valid",play))
for play in test_en:
    shutil.copyfile(os.path.join("./data/EN",play),os.path.join("./data/EN/test",play))
