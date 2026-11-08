# Task 1 — Asynchronous File Sorter

## Requirements

- Python 3.12
- Dependencies from requirements.txt

## Installation

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the script from the `task_1` directory:

```bash
python sort_files.py ./source ./output
```

The script recursively scans the source directory and copies files into subfolders grouped by extension.

Files without an extension are placed in the `no_extension` folder.


# Task 2 — MapReduce Word Frequency Analysis

## Description

This Python script downloads text from a specified URL, analyzes word frequency using the MapReduce paradigm and visualizes the top 10 most frequently used words.

The program uses multithreading with `ThreadPoolExecutor` to process word frequency data.

## Requirements

* Python 3.14
* matplotlib
* requests

## Installation

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python visualize_top_words.py
```

The script downloads text from Project Gutenberg, calculates word frequencies, prints the top 10 most frequent words and displays a bar chart.

The chart is also saved as `top_words.png` in the current working directory.
