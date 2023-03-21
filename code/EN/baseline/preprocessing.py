import re
import logging
from nltk.tokenize import word_tokenize
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)


# Assumption: The files are already in SamSum data format
def open_file(f_name: str) -> str:
    '''
    To read the file and remove any additional spaces in the lines, and
    create a basic tokenization for the data. Also, for some files,
    characters name are all caps in utterance, Normalising that as well.
    '''
    logging.info(f"Reading {f_name.split('/')[-1]} for processing")
    lines = []
    with open(f_name, 'r', encoding='utf-8') as obj:
        for line in obj:
            if line.strip():
                tok_line = word_tokenize(line)
                tok_line[0] = tok_line[0].title()
                lines.append(" ".join(tok_line))
    return "\n".join(lines)


def make_chunks(sentence_list: list) -> list:
    logging.info("Creating chunks")
    chunk_size = 768
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


def split_data(text: str) -> list:
    '''
    To split the data into multiple segments, based on following criterions
    SCENE_CHANGE, SCENE_END
    '''
    logging.info("Splitting the input")
    standardized_segments = []
    if "[SCENE_CHANGE]" in text:
        segments = re.split(r'\[SCENE_CHANGE\]', text)
    elif "SCENE_END" in text:
        segments = re.split(r'SCENE_END', text)
    else:
        segments = [text]
    for seg in segments:
        standardized_segments.extend(make_chunks(seg.splitlines()))
    return standardized_segments
