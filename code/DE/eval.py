import evaluate
import argparse
import os
import re

parser = argparse.ArgumentParser("Evaluate a single play with BERTScore, BLEU & ROUGE!")
parser.add_argument("--reference_path", help="Path to directory where references summaries are stored. File names should contain string 'sum'")
parser.add_argument("--candidate_path", help="Path to directory where generated summaries are stored (split into chunks)")

# Initialize Argument Parser:
args = parser.parse_args()

# Loading metrics.
print("Loading metrics...", end="")
rouge = evaluate.load("rouge")
bleu = evaluate.load("bleu")
bertscore = evaluate.load("bertscore")
print("Done")

references_path = args.reference_path
summary_path = args.candidate_path

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

summary = read_candidates(cand_path=summary_path)
refs = []
refs_paths = [os.path.join(references_path, file) for file in os.listdir(references_path) if "sum" in file]

for refp in refs_paths:
    with  open(refp, "r", encoding="utf-8") as ref_f:
        ref = ref_f.read()
        refs.append(ref)

print("Computing metrics...")
rouge_results = rouge.compute(predictions=[summary],
                        references=[refs])
bleu_results = bleu.compute(predictions=[summary], references=[refs], max_order=3)
bertscore_results = bertscore.compute(predictions=[summary], references=[refs], lang="de")

all_results = [("ROUGE", rouge_results), ("BLEU", bleu_results), ("BERTScore", bertscore_results) ]

for name, result in all_results:
    print(name)
    for key, value in result.items():
        print("{}:\t{}".format(key, value))
    print("==="*30)