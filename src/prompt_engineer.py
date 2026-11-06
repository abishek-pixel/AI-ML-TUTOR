"""Prompt engineering with multiple techniques."""
from typing import Dict, List, Tuple
from src.llm_client import LLMClient

class PromptEngineer:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def create_zero_shot_prompt(self, term: str, level: str) -> str:
        """Create zero-shot prompt."""
        return f"""Explain the AI/ML/DL concept "{term}" at a {level} level.

Provide a clear, concise explanation suitable for someone at the {level} level.
Include a comparison table with 3 related concepts."""
    
    def create_few_shot_prompt(self, term: str, level: str) -> str:
        """Create few-shot prompt with examples."""
        examples = {
            "school": "Example: Neural Network at school level - Think of it like your brain! Just as your brain has neurons that fire when you learn, artificial neural networks have nodes that learn patterns from data.",
            "UG": "Example: Neural Network at UG level - A computational model inspired by biological neurons, consisting of interconnected layers that transform inputs through weighted connections and activation functions.",
            "expert": "Example: Neural Network at expert level - A parameterized differentiable function f(x;θ) comprising hierarchical representations learned via gradient-based optimization on a loss landscape."
        }
        
        return f"""Explain AI/ML/DL concepts at different levels.

{examples.get(level, examples['UG'])}

Now explain "{term}" at {level} level with a comparison table of 3 related concepts."""
    
    def create_chain_of_thought_prompt(self, term: str, level: str) -> str:
        """Create chain-of-thought prompt."""
        return f"""Let's break down the concept "{term}" step by step for a {level} level explanation:

Step 1: Identify the core idea of {term}
Step 2: Explain how it works in simple terms
Step 3: Describe its key components
Step 4: Show practical applications
Step 5: Compare with 3 related concepts in a table

Please work through each step systematically."""
    
    def evaluate_response(self, response: str) -> float:
        """Simple scoring based on response quality."""
        score = 0.0
        
        # Check length (good explanations are comprehensive)
        if len(response) > 200:
            score += 0.3
        
        # Check for structure (paragraphs)
        if response.count('\n\n') >= 2:
            score += 0.2
        
        # Check for comparison table indicators
        table_keywords = ['|', 'comparison', 'table', 'vs', 'difference']
        if any(kw in response.lower() for kw in table_keywords):
            score += 0.3
        
        # Check for technical terms
        tech_keywords = ['model', 'algorithm', 'data', 'learning', 'network', 'function']
        score += min(0.2, sum(0.04 for kw in tech_keywords if kw in response.lower()))
        
        return min(1.0, score)
    
    def compare_techniques(self, term: str, level: str, temperature: float) -> Dict:
        """Compare all three prompt techniques."""
        results = {}
        
        # Zero-shot
        zero_prompt = self.create_zero_shot_prompt(term, level)
        zero_response = self.llm.generate(zero_prompt, temperature)
        results['zero_shot'] = {
            'prompt': zero_prompt,
            'response': zero_response,
            'score': self.evaluate_response(zero_response)
        }
        
        # Few-shot
        few_prompt = self.create_few_shot_prompt(term, level)
        few_response = self.llm.generate(few_prompt, temperature)
        results['few_shot'] = {
            'prompt': few_prompt,
            'response': few_response,
            'score': self.evaluate_response(few_response)
        }
        
        # Chain-of-thought
        cot_prompt = self.create_chain_of_thought_prompt(term, level)
        cot_response = self.llm.generate(cot_prompt, temperature)
        results['chain_of_thought'] = {
            'prompt': cot_prompt,
            'response': cot_response,
            'score': self.evaluate_response(cot_response)
        }
        
        return results
