# import pytest
import spacy
from collections import defaultdict

# Load SpaCy model
nlp = spacy.load("en_core_web_lg")

# Import the functions from your main script
from redactor import redact_names, redact_dates, redact_phones, redact_addresses, redact_concepts

# Test cases for redact_names
def test_redact_names():
    stats = defaultdict(int)
    doc = nlp("John Doe and Jane Smith are meeting at the park.")
    result = redact_names(doc, stats)
    assert "████████ and ██████████ are meeting at the park." in result
    assert stats['names'] == 2

# Test cases for redact_dates
def test_redact_dates():
    stats = defaultdict(int)
    text = "The meeting is on 15 Jan 2024 and the deadline is 2024-01-15."
    result = redact_dates(text, stats)
    assert "The meeting is on ███████████ and the deadline is ██████████." in result
    assert stats['dates'] == 2

# Test cases for redact_phones
def test_redact_phones():
    stats = defaultdict(int)
    text = "Call me at 123-456-7890 or +1 (987) 654-3210."
    result = redact_phones(text, stats)
    assert "Call me at ████████████ or +1 (█████████████." in result
    assert stats['phones'] == 2

def test_redact_addresses():
    stats = defaultdict(int)
    text = "I live at 123 Main St. and work at 456 Elm Avenue."
    result = redact_addresses(text, stats)
    assert "I live at ████████████ and work at ███████████████" in result
    assert stats['addresses'] == 2

# Test cases for redact_concepts
def test_redact_concepts():
    stats = defaultdict(int)
    doc = nlp("The school is closed today. The hospital is open 24/7.")
    concepts = ["school", "hospital"]
    result = redact_concepts(doc, concepts, stats)
    assert "███████████████████████████ ██████████████████████████" in result
    assert stats['concepts'] == 2

# Run all tests
# if __name__ == "__main__":
#     pytest.main([__file__])