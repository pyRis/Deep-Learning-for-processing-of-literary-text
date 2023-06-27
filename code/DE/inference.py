import argparse
import os

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, set_seed

def make_chunks(sentence_list: list) -> list:
    chunk_size = 500
    count = 0
    sentences_in_chunk = []
    chunk = []
    for idx, sent in enumerate(sentence_list):
        count += len(sent.split())
        if count > chunk_size:
            sentences_in_chunk.append("".join(chunk))
            count = 0
            chunk = []
        else:
            chunk.append(sent)
    sentences_in_chunk.append("".join(chunk))
    return sentences_in_chunk

def create_summary(chunks: list, checkpoint_path: str) -> str:
    """Create summary for each segment."""
    device = torch.device("cpu")
    set_seed(42)
    model_checkpoint = checkpoint_path
    model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
    model.to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    summaries = []
    for chunk in chunks:
        segmented_summ = []
        for item in chunk:
            print(len(item))
            utterance = tokenizer(item, return_tensors="pt").to(device)
            summary = tokenizer.decode(
                model.generate(**utterance)[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )
            segmented_summ.append(summary)
        summaries.append("".join(segmented_summ))
    return "\n".join(summaries)

def read_chunk_files(path: str, prefix_filename="chunk") -> list:
    play_files = [os.path.join(path, file) for file in os.listdir(path) if prefix_filename in file]
    chunks_final = []
    for chunk in play_files:
        with open(chunk, encoding="utf-8") as f:
            content = f.readlines()
            chunks = make_chunks(content)
            chunks_final.append(chunks)
    return chunks_final

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

