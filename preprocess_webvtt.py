import webvtt
import re
import glob
import os
import argparse
from typing import List
import helpers.logging
from structlog import BoundLogger


def process_vtt(file: str, log: BoundLogger):
    all_caps: bool = True
    newline_in_previous: bool = False
    try:
        with open(f"{file}.vtt", "w", encoding="utf-8") as f:
            for caption in webvtt.read(file):
                if re.search(r"[a-z]", caption.text):
                    all_caps = False
                fragment: str = ""
                fragment += f"⎡⎡{caption.start} --> {caption.end}⎦⎦ "
                # multiple speakers
                if caption.raw_text.startswith("-"):
                    fragment += (
                        "\n".join(
                            re.sub(r"^-(\s*[A-Z]+:)?", r"⎡⎡Speaker \1⎦⎦ ", line)
                            for line in caption.lines
                        )
                        + " "
                    )
                else:
                    cue_text = " ".join(caption.raw_text.splitlines()) + " "
                    fragment += re.sub(r"^([A-Z]+:)", r"⎡⎡Speaker \1⎦⎦ ", cue_text)
                # sounds in brackets
                if re.match(r"^\[[^\]]*\]$", caption.raw_text) or re.match(
                    r"⎡⎡Speaker[^⎦]*?⎦⎦ *\[[^\]]*\]", caption.raw_text
                ):
                    if newline_in_previous:
                        fragment += "\n"
                    else:
                        fragment = "\n" + fragment + "\n"
                    newline_in_previous = True
                elif fragment.endswith("] "):
                    fragment += "\n"
                    newline_in_previous = True
                # break after punctuation
                elif re.search(r"[!?\.]$", caption.text):
                    fragment += "\n"
                    newline_in_previous = True
                else:
                    newline_in_previous = False
                f.write(re.sub(" +", " ", fragment))
    except Exception as e:
        log.exception("Processing error", file=file, error=str(e))
        raise Exception("Processing error") from e

    if all_caps:
        print("All captions are in uppercase.")


def main():
    parser = argparse.ArgumentParser(
        description="Process all .webvtt files in a folder."
    )
    parser.add_argument(
        "path", help="Path to the file, or folder containing .webvtt files"
    )
    args = parser.parse_args()
    path = args.path
    log = helpers.logging.create_log("preprocessing")
    log.info("Starting preprocessing", path=path)
    files: List[str] = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        pattern = os.path.join(path, "**", "*.webvtt")
        files.extend(glob.glob(pattern, recursive=True))
    else:
        log.exception("Invalid path", path=path)
        raise Exception(f"Path {path} is not valid.")
    log.info("Files", count=len(files))
    for vtt_file in files:
        process_vtt(vtt_file, log)


if __name__ == "__main__":
    main()
