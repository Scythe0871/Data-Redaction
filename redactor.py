import spacy
import re
import argparse
import os
from collections import defaultdict
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def redact_names(text, stats):
    doc = nlp(text)
    redacted_text = text
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE"]:
            redacted_text = redacted_text.replace(ent.text, "█" * len(ent.text))
            if ent.label_ == "PERSON" or "GPE":
                stats['names'] += 1
    return redacted_text

def redact_dates(text, stats):
    date_pattern = r'\b(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s[A-Za-z]+\s\d{4}|[A-Za-z]+\s\d{1,2},?\s\d{4}|\d{4}[-/]\d{2}[-/]\d{2})\b'
    redacted_text = text
    matches = re.finditer(date_pattern, redacted_text)
    for match in matches:
        date_string = match.group()
        redacted_text = redacted_text.replace(date_string, '█' * len(date_string))
        stats['dates'] += 1
    return redacted_text

def redact_phones(text, stats):
    results = analyzer.analyze(text=text, language='en')
    phone_results = [result for result in results if result.entity_type == 'PHONE_NUMBER']
    operator_config = OperatorConfig("replace", {"new_value": "█" * 10})
    anonymized_text = anonymizer.anonymize(
        text=text,
        analyzer_results=phone_results,
        operators={"PHONE_NUMBER": operator_config}
    )
    stats['phones'] += len(phone_results)
    return anonymized_text.text

def redact_addresses_with_security_stamps(text, stats):
    # Define the address regex pattern
    address_pattern = r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\.?'
    
    # Function to replace address with '█' characters of the same length
    def redact_address(match):
        address = match.group(0)
        stats['addresses'] += 1
        return '█' * len(address)

    # Replace matched addresses with '█' characters
    redacted_text = re.sub(address_pattern, redact_address, text)

    return redacted_text

def redact_concepts(text, concepts, stats):
    doc = nlp(text)
    analyzer_results = []
    for sent in doc.sents:
        for concept in concepts:
            if concept.lower() in sent.text.lower():
                analyzer_results.append(
                    RecognizerResult(
                        entity_type="CONCEPT",
                        start=sent.start_char,
                        end=sent.end_char,
                        score=1.0
                    )
                )
                stats['concepts'] += 1
                break  # Move to the next sentence after finding a match

    operator_config = OperatorConfig("replace", {"new_value": "█" * 10})
    anonymized_text = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators={"CONCEPT": operator_config}
    )
    return anonymized_text.text

def process_file(input_file, output_file, redact_flags, concepts, stats):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    redacted_text = text

    if 'names' in redact_flags:
        redacted_text = redact_names(redacted_text, stats)
    if 'dates' in redact_flags:
        redacted_text = redact_dates(redacted_text, stats)
    if 'phones' in redact_flags:
        redacted_text = redact_phones(redacted_text, stats)
    if 'address' in redact_flags:
        redacted_text = redact_addresses_with_security_stamps(redacted_text, stats)
    if concepts:
        redacted_text = redact_concepts(redacted_text, concepts, stats)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(redacted_text)

def write_stats(stats, stats_file):
    with open(stats_file, 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

def main():
    parser = argparse.ArgumentParser(description="Redact sensitive information from text files.")
    parser.add_argument("--names", action="store_true", help="Redact names and locations")
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
        import sys
        for key, value in stats.items():
            print(f"{key}: {value}", file=sys.stderr)
    elif args.stats == "stdout":
        for key, value in stats.items():
            print(f"{key}: {value}")
    else:
        write_stats(stats, args.stats)

if __name__ == "__main__":
    main()