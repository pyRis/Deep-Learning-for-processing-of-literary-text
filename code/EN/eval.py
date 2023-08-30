import evaluate
import argparse
import os
import re

def read_candidates(cand_path):
    candidates_files = [file for file in os.listdir(cand_path) if "chunk" in file and ".txt" in file]
    candidates_files.sort(key=lambda x: int(re.search("\d+", x).group(0)))
    candidates_content = []
    for file in candidates_files:
        file_path = os.path.join(cand_path, file)
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            candidates_content.append(content)
    return "\n".join(candidates_content)


rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")

language = "EN"
setting = "monolingual_EN"
model = "mT5-custom-only"

references_path = f"/Deep-Learning-for-processing-of-literary-text/data/EN/test"

with open("/results.txt","a") as f:
    # f.write(f"language\tsetting\tmodel\tplay\trouge1\trouge2\trougeL\trougeLsum\tBERTScore(p)\tBERTScore(r)\tBERTScore(F1)\n")
    for play in os.listdir(references_path):
        print(f"play:{play}")
        
        summary_path = f"/Deep-Learning-for-processing-of-literary-text/summary/{language}/{setting}/{model}/{play}"
        summary = read_candidates(cand_path=summary_path)

        plays_path = os.path.join(references_path, play)
        refs_paths = [os.path.join(plays_path, file) for file in os.listdir(plays_path) if "sum" in file]

        refs = []
        for refp in refs_paths:
            with  open(refp, "r", encoding="utf-8") as ref_f:
                ref = ref_f.read()
                refs.append(ref)

        print(f"refs_paths:{refs_paths}\nsummary_path:{summary_path}")

  
        rouge_results = rouge.compute(predictions=[summary],
                                references=[refs])
        bertscore_results = bertscore.compute(predictions=[summary], references=[refs], lang="en") #"en","de"

        rouges,bertscores = [],[]

        for key, value in rouge_results.items():
            rouges.append((key, round(value,2)))
        for key, value in bertscore_results.items():
            bertscores.append((key,value[0]))

        f.write(f"{language}\t{setting}\t{model}\t{play}\t{rouges[0]}\t{rouges[1]}\t{rouges[2]}\t{rouges[3]}\t{bertscores[0]}\t{bertscores[1]}\t{bertscores[2]}\n")
        