import re
import json
from tqdm import tqdm
import os

# list of regular expression to foarged in transcripts.
reg_ex = {
    r"( *)\<(.*?)\>": "",
    r"\n": "",
    r"(  +)": " ",
    r"\-": "",
    r"(,+)": ",",
    r"( *)(-+)": "",
    r"\[": "",
    r"\]": "",
}

# utility methods


# open transcript using given file_path
def open_transcript(file_path):
    document = open(file_path, "r").readlines()
    return document


# remove punctuations and special tokens
def rem_ntok(reg_ex, text):
    for key, val in reg_ex.items():
        text = re.sub(key, val, text)
    return text


# remove extra space from the text
# remove \n and concat utterance which do not start with (PERSON.*?)
# prev_sent = ''
def add_colon(sentence, id):
    eidx = re.search(r"\(PERSON(.*?)\)", sentence).end()
    try:
        if sentence[eidx] == ":":
            return sentence
        else:
            return sentence[:eidx] + ":" + sentence[eidx:]
        # prev_sent = sentence
    except:
        # print(prev_sent)
        print(sentence)
        exit()


# process roles list and remove "( and )"
def process_roles(role):
    regex = {r"\(": "", r"\)": ""}
    for key, value in regex.items():
        role = re.sub(key, "", role)
    return role


# remove special tokens from the processed list of roles and utterances
def remove_special_tokens(utterance):
    regex = [
        r"^\.\',",
        r"^\.\'",
        r"^\',",
        r"^,",
        r"^\'",
        r"^\.",
        r"^, ,",
        r"^\?",
    ]
    for exp in regex:
        utterance = re.sub(exp, "", utterance)
    return utterance


# retur max_lenght of list of sentences
def max_length(text_list):
    length = [len(text.split(" ")) for text in text_list]
    return max(length)


# remove short utterances precisely "4"
def preprocess_utterance(sequence):
    return_seq = [sentences for sentences in sequence if len(sentences) > 4]
    return return_seq


# insert extra roles based on generated sentences
def insert_to_roles(roles, len, idx, role, con_index):
    idx = idx + con_index
    for i in range(len):
        roles.insert(idx, role)
    return roles


# text insertion in utterance list at a particular position.
def insert_text(utterances, sequences, idx, con_index):
    idx = idx + con_index
    for text in sequences[::-1]:
        utterances.insert(idx, text)
    return utterances


# check if folder contains transcripts
def check_for_transcript(file_list):
    for file_ in file_list:
        result = re.findall("transcript", file_)
        if len(result) == 1:
            return file_
        else:
            pass
    return ValueError("File not found!")


# convert to json files and save
def to_JSON_batch(processed_dict, file_path):
    with open(file_path, "w") as file_handle:
        json.dump(processed_dict, file_handle)


def to_JSON_single(processed_dict, file_name, file_path):
    out_dict = {file_name: processed_dict}
    with open(file_path, "w") as file_handle:
        json.dump(out_dict, file_handle)


def anon(dc):
    doc = []
    for item in dc:
        doc.extend(item.split("\n"))
    person_dict = {}
    count = 0
    documents = []
    for line in doc:
        temp = line.split(":")

        documents.append(n_l)
    # print(documents)
    return documents, person_dict


# remove newline character
def preprocess_transcripts(document):
    # print(document)
    document = document.split("\n")
    transcript = [""]
    for line in document:
        if line == "\n":
            continue
        transcript.append(line.replace("\n", "") + " ")
    return document


# iterate over transcript and segmentation
def parse_transcript(reg_ex, transcript, id):
    updateList = [""]
    for text in transcript:
        updateList.append(rem_ntok(reg_ex=reg_ex, text=text))
    utteranceList = []
    person_regex = [r"\(PERSON(.*)\)"]
    # if id == "Doctor_Who_4":
    #     print(updateList)
    for text in updateList:
        result = re.findall(person_regex[0], text)
        if len(result) == 1 and (len(text.split()) > 1):
            utteranceList.append(add_colon(text, id))
        else:
            try:
                prev_text = utteranceList[-1]
                utteranceList[-1] = prev_text + text.strip() + " "
            except Exception as e:
                pass
    return utteranceList


# bifurcate transcripts into roles and utterances.
def split_transcripts(processed_transcript):
    roles, utterances, temp_roles = [], [], []
    for text in processed_transcript:
        temp = text.split(":")
        tune = remove_special_tokens(temp[1].strip()).strip()
        tune = remove_special_tokens(tune.strip()).strip()
        tune = remove_special_tokens(tune.strip()).strip()
        if tune != "" and len(tune) > 2:
            utterances.append(tune)
            temp_roles.append(temp[0])
    for role in temp_roles:
        roles.append(process_roles(role))
    return roles, utterances

    # shortning and splitting utterance sentence and assign roles!


def post_process(roles, utterances):
    mappings = {"idx": [], "utterances": [], "roles": []}
    for idx, utterance in enumerate(utterances):
        word_list = [sentence.strip() for sentence in utterance.split(" ")]
        sentence_list = [sentence.strip() for sentence in utterance.split(".")]
        # check if length of word list is greater than 150
        if len(word_list) > 150:
            sequence = []
            temp = ""
            for sentence in sentence_list:
                temp = f"{temp} {sentence}."
                # if word limit exceeded than create a new sentence
                if len(temp.split(" ")) > 150:
                    sequence.append(temp.strip())
                    temp = ""
            sequence.append(temp.strip())
            # delete the sentence present in original list
            del utterances[idx]
            # preprocess and striping and removing small sentence less than 3
            sequence = preprocess_utterance(sequence)
            len_roles = len(sequence)
            # retrieve corresponding role from the roles list
            role = roles[idx]
            # delete the role present in original list
            del roles[idx]
            # mapping index, roles and utterances to mapping dictionary
            mappings["idx"].append(idx)
            mappings["utterances"].append(sequence)
            mappings["roles"].append(role)
    # Applying modifications
    con_index = 0
    for idx, index in enumerate(mappings["idx"]):
        sequence = mappings["utterances"][idx]
        len_utterances = len(sequence)
        utterances = insert_text(utterances, sequence, index, con_index)
        roles = insert_to_roles(
            roles, len_utterances, index, mappings["roles"][idx], con_index
        )
        # Reflecting to the position of insertion
        # print(f'Inserted @ {index + con_index}')
        con_index = con_index + len_utterances

    # New length after insertion
    # print(f'Length of lists after insertion {len(roles), len(utterances)}')

    # Applying changes to main dictionary
    return roles, utterances


# process single file
def process_single(item, id1=99):
    transcripts = preprocess_transcripts(item)
    # print(transcripts)
    transcripts = parse_transcript(reg_ex, transcripts, id1)
    roles, utterances = split_transcripts(transcripts)
    roles, utterances = post_process(roles, utterances)
    trans_dict = {"meeting_id": id1, "roles": roles, "utterances": utterances}
    return trans_dict


# process batch files/ dataset
def batch_process(path_to_folder):
    folders = os.listdir(path_to_folder)
    main_dict = dict()
    for folder in tqdm(folders):
        try:
            root_folder = path_to_folder + f"{folder}/"
            files = os.listdir(root_folder)
            filename = check_for_transcript(files)
            trans_dict = process_single(f"{root_folder}{filename}")
            main_dict[folder] = trans_dict
        except Exception as e:
            pass
    return main_dict
