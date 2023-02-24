import re
from glob import glob


def preprocessing(file_name):
    """
    Function to clean the summary and replace dumb(smart) quotes with normal quotes
    """
    with open(file_name, "r", encoding="utf-8", errors="replace") as f:
        content = f.readlines()
    address = content[0]
    content[0] = ""
    for idx, val in enumerate(content):
        if "MY LATEST" in val:
            content[idx] = ""

        content[idx] = (
            val.replace("¡¯", "'").replace("��", "'").replace("’", "'").strip()
        )

    with open(f"{file_name}", "w", encoding="utf-8") as f:
        f.write((" ".join(content)).strip() + f"\n\n\nWebsite:\t{address}")


def main():
    files = glob("**/sum_*", recursive=True)
    for item in files:
        print(item)
        preprocessing(item)


if __name__ == "__main__":
    main()
