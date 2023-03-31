#!/usr/bin/env python3
from glob import glob
from os import path


def make_chunks(sentence_list: list) -> list:
    chunk_size = 768
    count = 0
    sentences_in_chunk = []
    chunk = []
    for idx, sent in enumerate(sentence_list):
        count += len(sent.split())
        if count >= chunk_size:
            sentences_in_chunk.append("".join(chunk))
            count = 0
            chunk = []
        chunk.append(sent)
    sentences_in_chunk.append("".join(chunk))
    return sentences_in_chunk


def main():
    files = glob("./DE/**/clean_text.txt", recursive=True)
    for item in files:
        f_path = path.dirname(item)
        with open(item, 'r') as f:
            content = f.readlines()
        all_chunks = make_chunks(content)
        for idx, chunk in enumerate(all_chunks):
            with open(f"{f_path}/chunk_{idx}.txt", 'w') as f:
                f.write(chunk)


if __name__ == "__main__":
    main()
