import torch
import sys
import re
from utils.utils import (
    gen_tsc,
    gen_summary,
)
from utils.processing import (
    process_single,
)


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json

device = torch.device("cuda")
ending = sys.argv[1]
out_dir = sys.argv[2]
model_checkpoint = sys.argv[3]


pattern = r"[\(\[].*?[\)\]]"

model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
model.to(device)
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

# Read the input

with open(ending, "r", encoding="utf-8") as f:
    content = f.readlines()
tran = [item.strip() for item in content]
# Do some preprocessing

person_dict = {}
set_speaker = []
fresh_line = []
fresh_fresh_line = []
id = 99
for i in tran:
    val = re.sub(pattern, "", i)
    if val.strip() and val[0] != "[" and val[0] != "(":
        fresh_line.append(val)
for val in fresh_line:
    temp = val.split(":")
    if 0 < len(temp[0].split()) < 4 and "," not in temp[0] and len(temp) == 2:
        temp[0] = temp[0].replace("-", "").strip()
        set_speaker.append(temp[0])
        val = " : ".join(temp)
        fresh_fresh_line.append(val)
set_speaker = list(set(set_speaker))
final_transcript = "\n".join(fresh_fresh_line)
count = 0
for val in set_speaker:
    person_dict[val] = f"(PERSON{count})"
    count += 1
for key in person_dict:
    final_transcript = final_transcript.replace(key, person_dict[key])

with open(f"person_mapping/{id}.json", "w+") as outfile:
    json.dump(person_dict, outfile)
final_transcript = final_transcript.replace(":", "")

tsc = process_single(final_transcript, id)

tsc_preprocessed = gen_tsc(tsc, tokenizer, 768)
s2, filename = gen_summary(tsc_preprocessed, model, tokenizer, out_dir)
summ = " ".join([item.strip() for item in s2[0]])
print(summ)
with open(f"summary/{id}.txt", "w+") as f:
    f.write(summ)
