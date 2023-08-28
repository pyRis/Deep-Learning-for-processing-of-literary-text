import evaluate
import argparse
import os
import re
from statistics import mean

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

def read_references(ref_path):
    refs = []
    refs_paths = [os.path.join(ref_path, file) for file in os.listdir(ref_path) if "sum" in file]
    for refp in refs_paths:
        with  open(refp, "r", encoding="utf-8") as ref_f:
            ref = ref_f.read()
            refs.append(ref)
    return refs

def compute_metrics(references, summaries):
    print("Computing metrics...")
    rouge_results = rouge.compute(predictions=summaries,
                            references=references)
    bleu_results = bleu.compute(predictions=summaries, references=references, max_order=3)
    bertscore_results = bertscore.compute(predictions=summaries, references=references, lang="de")
    bertscore_results = {k: mean(v) for k, v in bertscore_results.items() if all(isinstance(i, float) for i in v)}

    all_results = [("ROUGE", rouge_results), ("BLEU", bleu_results), ("BERTScore", bertscore_results) ]

    for name, result in all_results:
        print(name)
        for key, value in result.items():
            print("{}:\t{}".format(key, value))
        print("==="*30)

all_refs = os.listdir(references_path)
all_cand = os.listdir(summary_path)

references = []
candidates = []
for ref_dir in all_refs:
    if ref_dir not in all_cand:
        raise ValueError("Can't find candidates folder for {}".format(ref_dir))
    ref_path = os.path.join(references_path, ref_dir)
    cand_path = os.path.join(summary_path, ref_dir)
    current_candidate = read_candidates(cand_path=cand_path)
    current_ref = read_references(ref_path=ref_path)
    candidates.append(current_candidate)
    references.append(current_ref)

compute_metrics(references=references, summaries=candidates)