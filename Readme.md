# CIS 6930, Fall 2024 Project 1 (The Redactor)

## Overview

This Text Redaction Tool is a Python script designed to redact sensitive information from text files. It can identify and redact names, dates, phone numbers, addresses, and user-defined concepts. The tool uses SpaCy for natural language processing and regular expressions for pattern matching.

## Features

- Redact person names
- Redact dates in various formats
- Redact phone numbers
- Redact addresses
- Redact user-defined concepts (entire sentences containing specified keywords)
- Provide detailed statistics on redacted items

## Requirements

- Python 3.x
- SpaCy (with the 'en_core_web_lg' model)
- argparse
- re (regular expressions)

## Installation

1. Clone this repository or download the script.
2. Install the required packages:
    - pip install spacy argparse
3. Download the SpaCy model:
    - python -m spacy download en_core_web_lg
    - python -m spacy download en_core_web_md
    - python -m spacy download en_core_web_sm

## Functions

### `redact_names(doc, stats)`
**Description:** Redacts all recognized personal names found in the given spaCy document object.
- **Parameters:**
  - `doc`: spaCy Document object
  - `stats`: Dictionary to track the number of names redacted.
- **Returns:** Text string with personal names redacted.

**Test Case:** Verify that all instances of personal names are replaced with the appropriate number of redaction marks (█), and the stats counter is accurate.

### `redact_dates(text, stats)`
**Description:** Redacts all dates from the text using regular expressions.
- **Parameters:**
  - `text`: String containing the original text.
  - `stats`: Dictionary to keep track of the number of dates redacted.
- **Returns:** Text string with dates redacted.

**Test Case:** Ensure that various date formats are detected and redacted correctly, and the statistics are properly updated.

### `redact_phones(text, stats)`
**Description:** Redacts phone numbers from the text using regular expressions.
- **Parameters:**
  - `text`: String of text to process.
  - `stats`: Dictionary for recording the number of phone numbers redacted.
- **Returns:** Text with phone numbers redacted.

**Test Case:** Check that multiple phone number formats are recognized and redacted, and stats reflect the correct counts.

### `redact_addresses(text, stats)`
**Description:** Redacts physical addresses based on common address patterns.
- **Parameters:**
  - `text`: Text to be processed.
  - `stats`: Dictionary tracking number of addresses redacted.
- **Returns:** Text with addresses redacted.

**Test Case:** Validate that addresses are redacted entirely, including complex cases, and statistics are updated.

### `redact_concepts(doc, concepts, stats)`
**Description:** Redacts sentences containing specified concepts.
- **Parameters:**
  - `doc`: spaCy Document object.
  - `concepts`: List of strings, each representing a concept to redact.
  - `stats`: Dictionary to record the number of concept instances redacted.
- **Returns:** Text with relevant sentences redacted.

**Test Case:** Ensure that sentences containing the specified concepts are fully redacted, and stats are correctly counted.

### `process_file(input_file, output_file, redact_flags, concepts, stats)`
**Description:** Orchestrates the file reading, redacting, and writing process.
- **Parameters:** Detailed in the script.
- **Returns:** None; outputs redacted text to a file.

**Test Case:** Simulate processing of a complete file with mixed content to ensure all specified types of sensitive information are correctly redacted.

### `write_stats(stats, stats_file)`
**Description:** Writes the statistics of the redaction process to a specified file or output.
- **Parameters:** Stats dictionary and a file path or descriptor.
- **Returns:** None; outputs stats to the designated location.

**Test Case:** Confirm that the statistics are written accurately and in the correct format.

## Usage

Run the script from the command line with the following syntax:
    - python redactor.py [OPTIONS]

### Options:

- `--names`: Redact person names
- `--dates`: Redact dates
- `--phones`: Redact phone numbers
- `--address`: Redact addresses
- `--concept CONCEPT`: Redact sentences containing this concept (can be used multiple times for different concepts)
- `--stats STATS`: Specify where to write statistics (file path, 'stdout', or 'stderr', default is 'stderr')

### Example:
    - python redactor.py --names --dates --phones --address --concept confidential --concept sensitive --stats output_stats.txt

This command will redact names, dates, phone numbers, addresses, and sentences containing the words "confidential" or "sensitive", and write the statistics to 'output_stats.txt'.

## Input and Output

- The script reads from 'docs/input.txt'
- The redacted text is written to 'docs/output.txt'
- Statistics are written to the specified location (file, stdout, or stderr)

## Functions

1. `redact_names(doc, stats)`: Redacts person names using SpaCy's named entity recognition.
2. `redact_dates(text, stats)`: Redacts dates using regex patterns.
3. `redact_phones(text, stats)`: Redacts phone numbers using regex patterns.
4. `redact_addresses(text, stats)`: Redacts addresses using regex patterns.
5. `redact_concepts(doc, concepts, stats)`: Redacts entire sentences containing specified concepts.
6. `process_file(input_file, output_file, redact_flags, concepts, stats)`: Processes the input file and applies all specified redactions.
7. `write_stats(stats, stats_file)`: Writes redaction statistics to the specified output.

## Statistics Output

The statistics output includes:
- Counts for each type of redacted item (names, dates, phones, addresses, concepts)
- Detailed information for each redacted item, including:
  - Type of redaction
  - Start index in the original text
  - End index in the original text
  - Original content that was redacted

## Notes

- The script currently assumes that the input file is UTF-8 encoded.
- The address redaction may not catch all possible address formats. Adjust the regex pattern in `redact_addresses` if needed.
- Concept redaction works on a sentence level, so it may redact more text than strictly necessary if the concept word appears in a long sentence.



