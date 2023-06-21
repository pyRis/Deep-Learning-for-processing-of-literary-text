import argparse
import os

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, set_seed

def create_summary(segments: list, checkpoint_path: str) -> str:
    """Create summary for each segment."""
    device = torch.device("cuda")
    set_seed(42)
    model_checkpoint = checkpoint_path
    model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
    model.to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    segmented_summ = []
    for item in segments:
        utterance = tokenizer(item, return_tensors="pt").to(device)
        summary = tokenizer.decode(
            model.generate(**utterance)[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )
        segmented_summ.append(summary)
    return "".join(segmented_summ)

def read_chunk_files(path: str, prefix_filename="chunk") -> list:
    play_files = [os.path.join(path, file) for file in os.listdir(path) if prefix_filename in file]
    chunks = []
    for chunk in play_files:
        with open(chunk, encoding="utf-8") as f:
            content = f.read()
            chunks.append(content)
    return chunks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", help="Path to where chunk files are stored")
    parser.add_argument("--model", help="Path to model checkpoint")
    parser.add_argument("--output_path", help="Path where output should be stored")
    args = parser.parse_args()
    chunks = read_chunk_files(args.input_path)
    summary = create_summary(chunks, args.model)
    with open(args.output_path, "w", encoding="utf-8") as out_f:
        out_f.write(summary)

if __name__ == "__main__":
    main()

