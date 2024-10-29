def test_phones():
    test_cases = [
        ("Call me at 123-456-7890 for more information.", 
         "Call me at ██████████ for more information."),
        
        ("My office number is (123) 456-7890.", 
         "My office number is ██████████."),
        
        ("You can reach her at 1234567890 or 987-654-3210.", 
         "You can reach her at ██████████ or ██████████."),
        
        ("International number: +1 (123) 456-7890.", 
         "International number: ██████████."),
        
        ("Phone: 123.456.7890 or 123 456 7890.", 
         "Phone: ██████████ or ██████████."),
        
        ("Multiple numbers: 123-456-7890, (987) 654-3210, and 1231231234.", 
         "Multiple numbers: ██████████, ██████████, and ██████████."),
        
        ("No phone number here, just text.", 
         "No phone number here, just text."),
        
        ("Partial number: 123-456", 
         "Partial number: 123-456")
    ]
    return test_cases

# To run the test cases:
test_cases = test_phones()
for input_text, expected_output in test_cases:
    print(f"Input: {input_text}")
    print(f"Expected Output: {expected_output}")
    print("---")