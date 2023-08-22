import evaluate
import os

rouge = evaluate.load("rouge")

references_path = "data/DE/test/Romeo_und_Julia"
summary_path = "summary/DE/finetuned/Romeo_und_Julia.txt"

with open(summary_path, "r", encoding="utf-8") as sum_f:
    summary = sum_f.read()

refs = []
refs_paths = [os.path.join(references_path, file) for file in os.listdir(references_path) if "sum" in file]

for refp in refs_paths:
    with  open(refp, "r", encoding="utf-8") as ref_f:
        ref = ref_f.read()
        refs.append(ref)

results = rouge.compute(predictions=[summary],
                        references=[refs])

# baseline: {'rouge1': 0.3305853256389118, 'rouge2': 0.03465346534653465, 'rougeL': 0.10140148392415499, 'rougeLsum': 0.3206924979389942}
# 

print(results)