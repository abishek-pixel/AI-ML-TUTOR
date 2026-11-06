"""Chat manager with conversation memory and attention visualization."""
from typing import List, Dict, Tuple
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from PIL import Image

class ChatManager:
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only recent messages
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.conversation_history
    
    def get_context_string(self) -> str:
        """Get conversation history as formatted string."""
        context = []
        for msg in self.conversation_history[-6:]:  # Last 3 exchanges
            context.append(f"{msg['role'].upper()}: {msg['content']}")
        return "\n".join(context)
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def generate_attention_heatmap(self, query: str) -> Image.Image:
        """Generate attention heatmap for user query.
        
        Simulates attention weights between query tokens and context.
        In a real implementation, this would extract actual attention weights
        from the transformer model.
        """
        # Tokenize query (simple word split for demo)
        query_tokens = query.split()[:10]  # Limit tokens
        
        # Get recent context
        context_text = self.get_context_string()
        context_tokens = context_text.split()[-15:] if context_text else ["[START]"]
        
        # Simulate attention weights (in production, get from model)
        attention_weights = self._simulate_attention(query_tokens, context_tokens)
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.heatmap(
            attention_weights,
            xticklabels=context_tokens,
            yticklabels=query_tokens,
            cmap='YlOrRd',
            annot=False,
            fmt='.2f',
            cbar_kws={'label': 'Attention Weight'},
            ax=ax
        )
        
        ax.set_title('Attention Heatmap: Query vs Context', fontsize=14, fontweight='bold')
        ax.set_xlabel('Context Tokens', fontsize=12)
        ax.set_ylabel('Query Tokens', fontsize=12)
        
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        # Convert to PIL Image
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()
        
        return img
    
    def _simulate_attention(self, query_tokens: List[str], context_tokens: List[str]) -> np.ndarray:
        """Simulate attention weights based on token similarity.
        
        In production, extract actual attention weights from transformer layers.
        """
        n_query = len(query_tokens)
        n_context = len(context_tokens)
        
        # Create attention matrix
        attention = np.random.rand(n_query, n_context) * 0.3
        
        # Add higher weights for matching/similar tokens
        for i, q_token in enumerate(query_tokens):
            for j, c_token in enumerate(context_tokens):
                if q_token.lower() == c_token.lower():
                    attention[i, j] += 0.6
                elif q_token.lower() in c_token.lower() or c_token.lower() in q_token.lower():
                    attention[i, j] += 0.3
        
        # Normalize to sum to 1 for each query token
        attention = attention / (attention.sum(axis=1, keepdims=True) + 1e-8)
        
        return attention
