[![Tests](https://github.com/JanHusarcik/webvtt_loc/actions/workflows/python-app.yml/badge.svg)](https://github.com/JanHusarcik/webvtt_loc/actions/workflows/python-app.yml)

# preprocess_webvtt.py

A utility script to process all `.webvtt` subtitle files in a specified folder (or a specific file), transforming their content and saving the results as new `.vtt` file(s).

## Features

- Based on provided argument
	- Recursively finds all `.webvtt` files in a given directory
	- Works with single `.webvtt` file
- Processes each caption:
  - Adds a custom timestamp marker.
  - Joins multi-line captions.
  - Handles speaker lines and special formatting.
  - Detects if all captions are uppercase.
- Outputs processed captions to new files with a `.vtt` extension (e.g., `input.webvtt` → `input.webvtt.vtt`).

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Testing

Use `uv run -m pytest` to run the tests.

## Usage

```bash
uv run preprocess_webvtt.py /path/to/folder
```

- Replace `path\to\folder` with the directory containing your `.webvtt` files.
- The script will process all `.webvtt` files found recursively in the folder.

or

```bash
uv run preprocess_webvtt.py /path/to/file.webvtt
```

- Replace `/path/to/file.webvtt` with the path of the specific `.webvtt` file.
- The script will process the `.webvtt` file.



## Output

- For each input file `filename.webvtt`, a processed file `filename.webvtt.vtt` will be created in the same directory.

## Example

```
uv run preprocess_webvtt.py c:\subtitles
```

This will process all `.webvtt` files under the `c:\subtitles` directory and its subdirectories.

## License

MIT License

