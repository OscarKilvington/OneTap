from app.api_test import run_tests

if __name__ == "__main__":
    test_prompts = [
        "Write a haiku about artificial intelligence.",
        "Explain quantum computing in simple terms.",
        "What are the three laws of robotics?"
    ]
    
    run_tests(test_prompts)