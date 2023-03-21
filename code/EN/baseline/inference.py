"""Code for inference."""
import torch
import sys
from preprocessing import (
    open_file, split_data
)
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, set_seed


def create_summary(segments: list) -> str:
    """Create summary for each segment."""
    device = torch.device("cuda")
    set_seed(42)
    model_checkpoint = sys.argv[3]
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


def main() -> None:
    """Driver function to create the summary."""
    inp = sys.argv[1]
    file_name = inp.split("/")[-2]
    out_dir = sys.argv[2]
    sentence_list = open_file(inp)
    segments = split_data(sentence_list)
    summary = create_summary(segments)
    with open(f"{out_dir}/{file_name}_summary.txt", "w", encoding='utf-8') as f:
        f.write(summary)


if __name__ == "__main__":
    main()