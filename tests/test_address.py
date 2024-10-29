def test_addresses():
    test_cases = [
        ("I live at 123 Main Street, Anytown, USA 12345.", 
         "I live at ████████████████, Anytown, USA 12345."),
        
        ("The office is located at 456 Elm Avenue, Suite 789, Big City, State 67890.", 
         "The office is located at ██████████████, Suite 789, Big City, State 67890."),
        
        ("Send mail to: 789 Oak Rd., Small Town, ST 54321.", 
         "Send mail to: ███████████, Small Town, ST 54321."),
        
        ("Multiple addresses: 123 Pine St. and 456 Maple Ave.", 
         "Multiple addresses: ████████████ and ███████████████."),
        
        ("Visit us at 1 Corporate Plaza, 10th Floor, Metropolis, NY 00001.", 
         "Visit us at ███████████████████, 10th Floor, Metropolis, NY 00001."),
        
        ("The new location is 42 Wallaby Way, Sydney.", 
         "The new location is ████████████████, Sydney."),
        
        ("No address here, just text.", 
         "No address here, just text."),
        
        ("Partial address: 123 Main", 
         "Partial address: 123 Main")
    ]
    return test_cases

# To run the test cases:
test_cases = test_addresses()
for input_text, expected_output in test_cases:
    print(f"Input: {input_text}")
    print(f"Expected Output: {expected_output}")
    print("---")