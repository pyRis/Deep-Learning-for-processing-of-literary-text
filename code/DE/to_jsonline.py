import os
import argparse
import json 

parser = argparse.ArgumentParser("Convert chunks into jsonline format")
parser.add_argument("--input_dir")
parser.add_argument("--out_path")


args = parser.parse_args()

in_dir = args.input_dir
out_path = args.out_path

chunk_files = [file for file in os.listdir(in_dir) if "chunk_" in file] 
chunk_files = sorted(chunk_files, key=lambda x: int(x.split("_")[-1].strip(".txt")))

json_lines = []

for file_name in chunk_files:
    f_path = os.path.join(in_dir, file_name)
    with open(f_path, encoding="utf-8") as file:
        content = file.read().replace("\n", " ")
        json_dict = {"text": content, "summary": "Some summary."}
        json_lines.append(json_dict)

with open(out_path, "w", encoding="utf-8") as out_f:
    for line in json_lines:
        str_json = json.dumps(line)
        out_f.write(f"{str_json}\n")


