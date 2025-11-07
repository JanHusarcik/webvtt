import argparse
from typing import List
import glob
import os
import helpers.logging
import helpers.postprocess
import helpers.preprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import alive_progress

MAX_CONCURRENT = 4  # Adjust as needed


def process_with_semaphore(func, vtt_file, log, semaphore):
    with semaphore:
        func(vtt_file, log)


def main():
    parser = argparse.ArgumentParser(description="Process .webvtt files.")
    parser.add_argument(
        "path", help="Path to the file, or folder containing .webvtt files"
    )
    parser.add_argument(
        "action", help="What to do with the files", choices={"prepare", "finalize"}
    )
    args = parser.parse_args()
    log = helpers.logging.create_log(args.action)
    path = args.path
    log.info("Starting", action=args.action, path=path)
    files: List[str] = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        pattern = os.path.join(path, "**", "*.webvtt")
        files.extend(glob.glob(pattern, recursive=True))
    else:
        log.exception("Invalid path", path=path)
        raise Exception(f"Path {path} is not valid.")

    semaphore = threading.Semaphore(MAX_CONCURRENT)
    executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT)
    futures = []

    if args.action == "prepare":
        for vtt_file in files:
            futures.append(
                executor.submit(
                    process_with_semaphore,
                    helpers.preprocess.process_vtt,
                    vtt_file,
                    log,
                    semaphore,
                )
            )
    if args.action == "finalize":
        for vtt_file in files:
            futures.append(
                executor.submit(
                    process_with_semaphore,
                    helpers.postprocess.process_vtt,
                    vtt_file,
                    log,
                    semaphore,
                )
            )
    with alive_progress.alive_bar(
        len(futures), title="Processing files", enrich_print=False
    ) as bar:
        for future in as_completed(futures):
            # Will raise exceptions if any occurred in the worker threads
            future.result()
            bar()

    log.info("Done.")


if __name__ == "__main__":
    main()
