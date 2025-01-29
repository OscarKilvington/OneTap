from openai import OpenAI
from anthropic import Anthropic
import aiohttp
from ..core.config import get_settings
from typing import List, Dict, Any, Optional

settings = get_settings()

class AIService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY
        
        # Model configurations
        self.models = {
            "gpt-4-turbo": {
                "provider": "openai",
                "capabilities": ["general"],
                "priority": 5
            },
            "gpt-3.5-turbo": {
                "provider": "openai",
                "capabilities": ["general"],
                "priority": 4
            },
            "claude-3-opus": {
                "provider": "anthropic",
                "capabilities": ["general"],
                "priority": 5
            },
            "claude-2.1": {
                "provider": "anthropic",
                "capabilities": ["general"],
                "priority": 4
            }
        }
    
    async def route_query(self, query: str, task_type: str) -> str:
        """Route the query to the most suitable model based on task type"""
        model = self._select_model(task_type)
        return await self.generate_response(query, model)
    
    def _select_model(self, task_type: str) -> str:
        """Select the best model for the given task type"""
        suitable_models = [
            (name, config) for name, config in self.models.items()
            if task_type in config["capabilities"]
        ]
        
        if not suitable_models:
            return "gpt-4"  # Default to GPT-4 if no specific model is suitable
            
        # Sort by priority and return the highest priority model
        return max(suitable_models, key=lambda x: x[1]["priority"])[0]
    
    def _calculate_openai_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for OpenAI API usage"""
        pricing = {
            "gpt-4-turbo": {"input": 0.01/1000, "output": 0.03/1000},
            "gpt-4": {"input": 0.03/1000, "output": 0.06/1000},
            "gpt-3.5-turbo": {"input": 0.0005/1000, "output": 0.0015/1000}
        }
        if model in pricing:
            return (input_tokens * pricing[model]["input"] + 
                    output_tokens * pricing[model]["output"])
        return 0.0

    def _calculate_anthropic_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for Anthropic API usage"""
        pricing = {
            "claude-3-opus": {"input": 0.015/1000, "output": 0.075/1000},
            "claude-3-sonnet": {"input": 0.003/1000, "output": 0.015/1000},
            "claude-2.1": {"input": 0.008/1000, "output": 0.024/1000}
        }
        if model in pricing:
            return (input_tokens * pricing[model]["input"] + 
                    output_tokens * pricing[model]["output"])
        return 0.0

    async def generate_response(self, query: str, model_name: str) -> Dict[str, Any]:
        """Generate response using the specified model"""
        import time
        start_time = time.time()
        
        model_config = self.models[model_name]
        provider = model_config["provider"]
        
        try:
            if provider == "openai":
                response, usage = await self._generate_openai_response(query, model_name)
                cost = self._calculate_openai_cost(
                    model_name,
                    usage["prompt_tokens"],
                    usage["completion_tokens"]
                )
                total_tokens = usage["total_tokens"]
            elif provider == "anthropic":
                response, usage = await self._generate_anthropic_response(query, model_name)
                cost = self._calculate_anthropic_cost(
                    model_name,
                    usage["input_tokens"],
                    usage["output_tokens"]
                )
                total_tokens = usage["input_tokens"] + usage["output_tokens"]
            elif provider == "deepseek":
                response = await self._generate_deepseek_response(query, model_name)
                cost = 0.0
                total_tokens = 0
            else:
                raise ValueError(f"Unknown provider: {provider}")
        except Exception as e:
            raise e
        finally:
            end_time = time.time()
            
        return {
            "content": response,
            "model": model_name,
            "provider": provider,
            "metrics": {
                "tokens_used": total_tokens,
                "cost_usd": cost,
                "latency_ms": (end_time - start_time) * 1000
            }
        }
    
    async def _generate_openai_response(self, query: str, model_name: str) -> tuple[str, dict]:
        """Generate response using OpenAI's API"""
        response = await self.openai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content, {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
    
    async def _generate_anthropic_response(self, query: str, model_name: str) -> tuple[str, dict]:
        """Generate response using Anthropic's API"""
        message = await self.anthropic_client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": query}]
        )
        return message.content[0].text, {
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens
        }
    
    async def _generate_deepseek_response(self, query: str, model_name: str) -> str:
        """Generate response using Deepseek's API"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": [{"role": "user", "content": query}]
                }
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]