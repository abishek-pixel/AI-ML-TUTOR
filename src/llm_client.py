"""LLM client for multiple providers."""
from typing import Dict, List, Optional
from src.config import Config

class LLMClient:
    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.api_key = Config.get_api_key()
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(Config.MODEL_NAME)
        elif self.provider == "groq":
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Generate response from LLM."""
        try:
            if self.provider == "gemini":
                response = self.client.generate_content(
                    prompt,
                    generation_config={"temperature": temperature, "max_output_tokens": max_tokens}
                )
                return response.text
            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_with_history(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Generate response with conversation history."""
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return self.generate(prompt, temperature)
