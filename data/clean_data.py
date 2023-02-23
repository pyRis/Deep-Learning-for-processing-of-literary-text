import re
from glob import glob


def preprocessing(file_name):
    """
    Function to remove lines with ***, exit (Exeunt), background information,
    Scene information etc
    """
    lines = []
    buffer = ""
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            if (
                re.match(r"^\*\*\*\*.*\*\*\*\*", line)
                or "Exeunt" in line
                or re.match(r"^Enter ", line)
                or "      " in line
                or not line.strip()
            ):
                continue
            elif (
                not line.startswith("  ")
                and "Shakespeare_homepage" not in line
            ):
                if buffer:
                    lines.append(buffer)
                buffer = line.strip() + ": "
            elif buffer:
                buffer = buffer + re.sub(r"\[.*?\]", "", line.strip()) + " "
    return lines


def main():
    """
    Driver function to run the preprocessing function
    """
    files = glob("**/full_text.txt", recursive=True)
    for item in files:
        new_f_name = item.replace("full_text", "clean_text")
        result = preprocessing(item)
        with open(new_f_name, "w", encoding="utf-8") as out:
            for line in result:
                out.write(line + "\n")


if __name__ == "__main__":
    main()

# ToDo: Add more cleaning to normalize text and remove things such as --, ;
