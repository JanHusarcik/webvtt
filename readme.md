[![Tests](https://github.com/JanHusarcik/webvtt_loc/actions/workflows/python-app.yml/badge.svg)](https://github.com/JanHusarcik/webvtt_loc/actions/workflows/python-app.yml)

# webvtt_loc

A utility for processing `.webvtt` subtitle files, supporting both preparation and finalization of captions for further use or publication.

## Features

- **Recursive and single-file processing**:  
  - Recursively finds all `.webvtt` files in a given directory, or processes a single file.
- **Two-stage workflow**:
  - **prepare**: Preprocesses captions for editing or review.
  - **finalize**: Postprocesses captions for final output.
- **Custom timestamp markers**:  
  - Adds custom markers to each caption for easier parsing.
- **Speaker and formatting handling**:  
  - Detects and formats speaker lines, including named and anonymous speakers.
  - Handles special formatting, such as sounds in brackets.
- **Line joining and wrapping**:  
  - Joins multi-line captions and wraps long lines to a configurable length (default: 36 characters).
- **Uppercase detection**:  
  - Detects if all captions are uppercase.
- **Output organization**:  
  - Writes processed captions to subfolders (`prepared` or `final`) in the original file's directory, preserving the original filename and extension.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python 3.8+

## Testing

Use `uv run -m pytest` to run the tests.

## Usage

```
uv run process_webvtt.py <path> <action>
```

- `<path>`: Path to a `.webvtt` file or a directory containing `.webvtt` files.
- `<action>`: Either `prepare` or `finalize`.

### Examples

Process all `.webvtt` files in a directory (preparation):

```
uv run process_webvtt.py /path/to/folder prepare
```

Process a single file and finalize:

```
uv run process_webvtt.py /path/to/file.webvtt finalize
```

## Output

- For each input file `filename.webvtt`:
  - The `prepare` action creates a processed file in a `prepared` subfolder:  
    `prepared/filename.webvtt`
  - The `finalize` action creates a processed file in a `final` subfolder:  
    `final/filename.webvtt`
- The original filename and extension are preserved in both cases.

## Details

### Preparation (`prepare` action)

- Adds custom timestamp markers:  
  `⎡⎡00:00:00.000 --> 00:00:01.000⎦⎦`
- Joins multi-line captions into a single line.
- Converts speaker lines (e.g., `- NAME:` or `-`) to a custom format:  
  - `- NAME:` → `⎡⎡Speaker NAME:⎦⎦`
  - `-` → `⎡⎡Speaker ⎦⎦`
- Handles sounds in brackets and breaks after punctuation.
- Detects and prints if all captions are uppercase.

### Finalization (`finalize` action)

- Reads preprocessed `.webvtt` files from the original location or the `prepared` subfolder.
- Splits and merges lines based on timestamp markers.
- Parses speaker tags and formats output:
  - If only one speaker in a caption, omits the `-` prefix.
  - For multiple speakers, each speaker line is prefixed with `-` or `- NAME:`.
- Wraps long lines to a maximum of 36 characters (configurable).
- Outputs finalized captions to the `final` subfolder, preserving the original filename and extension.

## License

MIT License
