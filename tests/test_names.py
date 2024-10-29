def test_names():
    test_cases = [
        ("Sam Alexis is transferring to Florida.", 
         "███ █████ is transferring to Florida."),
        
        ("Former University of Tennessee at Chattanooga forward Sam Alexis announced on his Instagram.", 
         "Former University of Tennessee at Chattanooga forward ███ █████ announced on his Instagram."),
        
        ("John Doe and Jane Smith attended the meeting.", 
         "████ ███ and ████ █████ attended the meeting."),
        
        ("The President of the United States is attending the summit.", 
         "The ████████ of the █████ █████ is attending the summit."),
        
        ("Elon Musk tweeted about the new technology.", 
         "████ ████ tweeted about the new technology.")
    ]
    return test_cases

# To run the test cases:
test_cases = test_names()
for input_text, expected_output in test_cases:
    print(f"Input: {input_text}")
    print(f"Expected Output: {expected_output}")
    print("---")