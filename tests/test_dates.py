def test_dates():
    test_cases = [
        ("The event is on 15 Jan 2024.", 
         "The event is on ███████████."),
        
        ("Meeting scheduled for 01/15/2024.", 
         "Meeting scheduled for ███████████."),
        
        ("The deadline is 2024-01-15.", 
         "The deadline is ███████████."),
        
        ("It happened on January 15, 2024.", 
         "It happened on ███████████████████."),
        
        ("Remember the date: 15 January 2024!", 
         "Remember the date: ████████████████!"),
        
        ("Multiple dates: 15 Jan 2024, 01/15/2024, and 2024-01-15.", 
         "Multiple dates: ███████████, ███████████, and ███████████."),
        
        ("No date here, just text.", 
         "No date here, just text."),
        
        ("Partial date: Jan 2024", 
         "Partial date: Jan 2024")
    ]
    return test_cases

# To run the test cases:
test_cases = test_dates()
for input_text, expected_output in test_cases:
    print(f"Input: {input_text}")
    print(f"Expected Output: {expected_output}")
    print("---")