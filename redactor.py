import spacy
import re
import argparse
import os
import sys
from collections import defaultdict

import en_core_web_lg
nlp = en_core_web_lg.load()

def redact_names(doc, stats):
    redacted_text = doc.text
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redacted_text = redacted_text.replace(ent.text, "█" * len(ent.text))
            stats['names'] += 1
    return redacted_text

def redact_dates(text, stats):
    date_pattern = r'\b(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s[A-Za-z]+\s\d{4}|[A-Za-z]+\s\d{1,2},?\s\d{4}|\d{4}[-/]\d{2}[-/]\d{2}|\d{1,2}/\d{1,2}/\d{1,2})\b'
    redacted_text = re.sub(date_pattern, lambda m: "█" * len(m.group()), text)
    stats['dates'] += len(re.findall(date_pattern, text))
    return redacted_text

def redact_phones(text, stats):
    phone_pattern = r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\d{5}-\d{5}\b'
    redacted_text = re.sub(phone_pattern, lambda m: "█" * len(m.group()), text)
    stats['phones'] += len(re.findall(phone_pattern, text))
    return redacted_text

def redact_addresses(text, stats):
    address_pattern = r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\.?|\d{4}\s[A-Z]{2}\s\d{2}[a-z]{2}\s[A-Z][a-z]'
    redacted_text = re.sub(address_pattern, lambda m: "█" * len(m.group()),text)
    stats['addresses'] += len(re.findall(address_pattern, text))
    return redacted_text
    
    # for sent in doc.sents:
    #     if re.search(address_pattern, sent.text, re.IGNORECASE):
    #         redacted_text.append('█' * len(sent.text))
    #         stats['addresses'] += 1
    #     else:
    #         redacted_text.append(sent.text)
    
    # return ' '.join(redacted_text)

def redact_concepts(doc, concepts, stats):
    redacted_text = []
    for sent in doc.sents:
        if any(concept.lower() in sent.text.lower() for concept in concepts):
            redacted_text.append('█' * len(sent.text))
            stats['concepts'] += 1
        else:
            redacted_text.append(sent.text)
    return ' '.join(redacted_text)

def process_file(input_file, output_file, redact_flags, concepts, stats):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    doc = nlp(text)
    redacted_text = text

    if 'names' in redact_flags:
        redacted_text = redact_names(doc, stats)
    if 'dates' in redact_flags:
        redacted_text = redact_dates(redacted_text, stats)
    if 'phones' in redact_flags:
        redacted_text = redact_phones(redacted_text, stats)
    if 'address' in redact_flags:
        redacted_text = redact_addresses(redacted_text, stats)
    if concepts:
        redacted_text = redact_concepts(nlp(redacted_text), concepts, stats)

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(redacted_text)
    except IOError:
        print(f"Error: Unable to write to output file '{output_file}'.")
        sys.exit(1)

def write_stats(stats, stats_file):
    try:
        with open(stats_file, 'w') as f:
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
    except IOError:
        print(f"Error: Unable to write to stats file '{stats_file}'.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Redact sensitive information from text files.")
    parser.add_argument("--names", action="store_true", help="Redact names")
    parser.add_argument("--dates", action="store_true", help="Redact dates")
    parser.add_argument("--phones", action="store_true", help="Redact phone numbers")
    parser.add_argument("--address", action="store_true", help="Redact addresses")
    parser.add_argument("--concept", action="append", help="Concepts to redact")
    parser.add_argument("--stats", help="File to write statistics to", default="stderr")
    
    args = parser.parse_args()
    
    input_file = os.path.join("docs", "input.txt")
    output_file = os.path.join("docs", "output.txt")
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    redact_flags = []
    if args.names:
        redact_flags.append('names')
    if args.dates:
        redact_flags.append('dates')
    if args.phones:
        redact_flags.append('phones')
    if args.address:
        redact_flags.append('address')

    stats = defaultdict(int)
    
    process_file(input_file, output_file, redact_flags, args.concept, stats)

    if args.stats == "stderr":
        for key, value in stats.items():
            print(f"{key}: {value}", file=sys.stderr)
    elif args.stats == "stdout":
        for key, value in stats.items():
            print(f"{key}: {value}")
    else:
        write_stats(stats, args.stats)

if __name__ == "__main__":
    main()