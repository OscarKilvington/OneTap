import os
import time
from openai import OpenAI
import anthropic
from dotenv import load_dotenv
from database import log_api_call, get_api_stats

load_dotenv()

class APIMetrics:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.tokens_used = 0
        self.cost = 0.0
        
    def start(self):
        self.start_time = time.time()
        
    def end(self):
        self.end_time = time.time()
        
    def get_latency(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0
    
    def calculate_openai_cost(self, model, input_tokens, output_tokens):
        # Current OpenAI pricing as of March 2024
        pricing = {
            "gpt-4-turbo-preview": {"input": 0.01/1000, "output": 0.03/1000},
            "gpt-4": {"input": 0.03/1000, "output": 0.06/1000},
            "gpt-3.5-turbo": {"input": 0.0005/1000, "output": 0.0015/1000}
        }
        if model in pricing:
            self.cost = (input_tokens * pricing[model]["input"] + 
                        output_tokens * pricing[model]["output"])
        self.tokens_used = input_tokens + output_tokens
        
    def calculate_claude_cost(self, model, input_tokens, output_tokens):
        # Current Anthropic pricing as of March 2024
        pricing = {
            "claude-3-opus": {"input": 0.015/1000, "output": 0.075/1000},
            "claude-3-sonnet": {"input": 0.003/1000, "output": 0.015/1000},
            "claude-2.1": {"input": 0.008/1000, "output": 0.024/1000}
        }
        if model in pricing:
            self.cost = (input_tokens * pricing[model]["input"] + 
                        output_tokens * pricing[model]["output"])
        self.tokens_used = input_tokens + output_tokens

def test_openai():
    client = OpenAI()
    metrics = APIMetrics()
    
    prompt = "Write a haiku about artificial intelligence."
    
    try:
        metrics.start()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        metrics.end()
        
        metrics.calculate_openai_cost(
            "gpt-3.5-turbo",
            response.usage.prompt_tokens,
            response.usage.completion_tokens
        )
        
        return {
            "success": True,
            "model": "gpt-3.5-turbo",
            "prompt": prompt,
            "response": response.choices[0].message.content,
            "metrics": {
                "latency": metrics.get_latency(),
                "tokens": metrics.tokens_used,
                "cost_usd": metrics.cost
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def test_anthropic():
    client = anthropic.Anthropic()
    metrics = APIMetrics()
    
    prompt = "Write a haiku about artificial intelligence."
    
    try:
        metrics.start()
        message = client.messages.create(
            model="claude-2.1",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        metrics.end()
        
        metrics.calculate_claude_cost(
            "claude-2.1",
            message.usage.input_tokens,
            message.usage.output_tokens
        )
        
        return {
            "success": True,
            "model": "claude-3-sonnet",
            "prompt": prompt,
            "response": message.content[0].text,
            "metrics": {
                "latency": metrics.get_latency(),
                "tokens": metrics.tokens_used,
                "cost_usd": metrics.cost
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def run_tests(prompts=None):
    if prompts is None:
        prompts = [
            "Write a haiku about artificial intelligence.",
            "Explain quantum computing in simple terms.",
            "What are the three laws of robotics?"
        ]
    
    results = []
    for prompt in prompts:
        print(f"\nTesting with prompt: {prompt}")
        print("-" * 50)
        
        # Test OpenAI
        print("\nOpenAI API:")
        openai_result = test_openai()
        log_api_call('openai', openai_result)
        print(f"Success: {openai_result['success']}")
        if openai_result['success']:
            print(f"Response: {openai_result['response']}")
            print(f"Metrics: {openai_result['metrics']}")
        else:
            print(f"Error: {openai_result['error']}")
        results.append(openai_result)
        
        # Test Anthropic
        print("\nAnthropic API:")
        anthropic_result = test_anthropic()
        log_api_call('anthropic', anthropic_result)
        print(f"Success: {anthropic_result['success']}")
        if anthropic_result['success']:
            print(f"Response: {anthropic_result['response']}")
            print(f"Metrics: {anthropic_result['metrics']}")
        else:
            print(f"Error: {anthropic_result['error']}")
        results.append(anthropic_result)
    
    # Print summary statistics
    stats = get_api_stats()
    print("\nOverall Statistics:")
    print("-" * 50)
    print(f"Total API calls: {stats['total_calls']}")
    print(f"Successful calls: {stats['successful_calls']}")
    print(f"Failed calls: {stats['failed_calls']}")
    print(f"Total cost (USD): ${stats['total_cost_usd']:.4f}")
    
    return results

if __name__ == "__main__":
    run_tests()