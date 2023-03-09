import os


def check_multi_lines(line):
    tokens = line.split(" ")
    sublines = []
    for token in tokens:
        if token.count("-") > 2:
            sublines.append("")
            sublines[-1] = sublines[-1] + token
        else:
            if len(sublines) == 0:
                continue
            else:
                sublines[-1] = sublines[-1] + " " + token
    if len(sublines) > 1:
        check = True
    else:
        check = False

    return check, sublines


def rem_punc(ctx):
    punc1 = """!()-[]{};:'"\,<>./?@#$%^&*_~"""
    for ele in ctx:
        if ele in punc1:
            ctx = ctx.replace(ele, "")
    return ctx


def jaccard(a, b):
    a = set(a)
    b = set(b)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def check_overlap(line1, line2):
    line1 = rem_punc(line1).split(" ")
    line2 = rem_punc(line2).split(" ")
    if line1[:2] == line2[:2]:
        return True
    else:
        jacc = jaccard(line1, line2)
        if jacc > 0.33:
            return True
        else:
            return False


def sort_multilines(log_tsc):
    line_ = log_tsc[0].replace("\n", "").split(" ")
    line_ = line_[0] + ": " + " ".join(line_[1:])
    corrected_logs = [line_]
    for i in range(1, len(log_tsc)):
        check, sublines = check_multi_lines(log_tsc[i])
        if log_tsc[i] == log_tsc[i - 1]:
            continue
        elif check:
            for i_ in range(len(sublines)):
                if sublines[i_] == sublines[i_ - 1]:
                    continue
                else:
                    line_ = sublines[i_].replace("\n", "").split(" ")
                    line_ = line_[0] + ": " + " ".join(line_[1:])
                    corrected_logs.append(line_)
        else:
            if len(sublines) == 0:
                corrected_logs[-1] = (
                    corrected_logs[-1] + " " + log_tsc[i].replace("\n", "")
                )
            else:
                line_ = log_tsc[i].replace("\n", "").split(" ")
                line_ = line_[0] + ": " + " ".join(line_[1:])
                corrected_logs.append(line_)

    return corrected_logs


def clean_multi_utterances(corrected_logs):
    speakers = [corrected_logs[0].split(": ")[0]]
    utterances = [corrected_logs[0].split(": ")[1]]
    for i in range(1, len(corrected_logs)):
        spk = corrected_logs[i].split(": ")[0]
        prev_spk = corrected_logs[i - 1].split(": ")[0]
        utt = corrected_logs[i].split(": ")[1]
        prev_utt = corrected_logs[i - 1].split(": ")[1]
        if spk != prev_spk:
            speakers.append(spk)
            utterances.append(utt)
        else:
            check = check_overlap(utt, prev_utt)
            if check:
                utterances[-1] = utt
            else:
                utterances[-1] = utterances[-1] + " " + utt

    return speakers, utterances


def replace_names(speakers):
    spk_dict = {}
    new_speakers = []
    for speaker in speakers:
        if speaker in spk_dict.keys():
            new_speakers.append(spk_dict[speaker])
        else:
            spk_dict[speaker] = "PERSON" + str(len(spk_dict) + 1)
            new_speakers.append(spk_dict[speaker])

    return new_speakers


def make_transcript(speakers, utterances):
    transcript = ""
    for s, u in zip(speakers, utterances):
        transcript = transcript + s + ": " + u + "\n"
    return transcript


def process_single_from_asr(path_to_file):
    with open(path_to_file, "r") as out:
        log_tsc = out.readlines()
    corrected_logs = sort_multilines(log_tsc)
    speakers, utterances = clean_multi_utterances(corrected_logs)
    speakers = replace_names(speakers)
    dir1, filename = os.path.split(path_to_file)
    id1 = filename.replace(".log", "")
    trans_dict = {
        "meeting_id": id1,
        "roles": speakers,
        "utterances": utterances,
    }

    return trans_dict


def gen_tsc_from_asr(log_tsc):
    corrected_logs = sort_multilines(log_tsc)
    speakers, utterances = clean_multi_utterances(corrected_logs)
    speakers = replace_names(speakers)
    transcript = make_transcript(speakers, utterances)

    return transcript
