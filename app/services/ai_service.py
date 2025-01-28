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
            "gpt-4": {
                "provider": "openai",
                "capabilities": ["programming", "math", "writing", "analysis"],
                "priority": 5
            },
            "claude-2": {
                "provider": "anthropic",
                "capabilities": ["programming", "analysis", "writing"],
                "priority": 4
            },
            "deepseek-coder": {
                "provider": "deepseek",
                "capabilities": ["programming"],
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
    
    async def generate_response(self, query: str, model_name: str) -> Dict[str, Any]:
        """Generate response using the specified model"""
        model_config = self.models[model_name]
        provider = model_config["provider"]
        
        if provider == "openai":
            response = await self._generate_openai_response(query, model_name)
        elif provider == "anthropic":
            response = await self._generate_anthropic_response(query, model_name)
        elif provider == "deepseek":
            response = await self._generate_deepseek_response(query, model_name)
        else:
            raise ValueError(f"Unknown provider: {provider}")
            
        return {
            "content": response,
            "model": model_name,
            "provider": provider
        }
    
    async def _generate_openai_response(self, query: str, model_name: str) -> str:
        """Generate response using OpenAI's API"""
        response = await self.openai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content
    
    async def _generate_anthropic_response(self, query: str, model_name: str) -> str:
        """Generate response using Anthropic's API"""
        message = await self.anthropic_client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": query}]
        )
        return message.content[0].text
    
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