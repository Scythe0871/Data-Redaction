def test_concepts():
    test_cases = [
        ("The children are playing in the school yard.", 
         "██████████████████████████████████████████."),
        
        ("Education is important for kids and adults alike.", 
         "██████████████████████████████████████████."),
        
        ("The new playground equipment arrived at the elementary school.", 
         "██████████████████████████████████████████████████████████."),
        
        ("This sentence doesn't contain any sensitive concepts.", 
         "This sentence doesn't contain any sensitive concepts."),
        
        ("Both schools and universities are educational institutions.", 
         "██████████████████████████████████████████████████."),
        
        ("The words 'school' and 'education' appear in this sentence.", 
         "██████████████████████████████████████████████████████."),
        
        ("Kids love to play and learn new things every day.", 
         "██████████████████████████████████████████."),
        
        ("The concept of learning is fundamental to growth.", 
         "██████████████████████████████████████████.")
    ]
    return test_cases

# To run the test cases:
test_cases = test_concepts()
for input_text, expected_output in test_cases:
    print(f"Input: {input_text}")
    print(f"Expected Output: {expected_output}")
    print("---")