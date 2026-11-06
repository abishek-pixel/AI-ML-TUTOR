"""Image processing with BLIP for diagram explanation."""
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from src.config import Config

class ImageProcessor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load BLIP model lazily."""
        try:
            print(f"Loading BLIP model on {self.device}...")
            self.processor = BlipProcessor.from_pretrained(Config.BLIP_MODEL)
            self.model = BlipForConditionalGeneration.from_pretrained(Config.BLIP_MODEL)
            self.model = self.model.to(self.device)
            print("BLIP model loaded successfully")
        except Exception as e:
            print(f"Error loading BLIP model: {e}")
            self.processor = None
            self.model = None
    
    def explain_diagram(self, image: Image.Image, context: str = "") -> str:
        """Generate explanation for uploaded diagram."""
        if self.model is None or self.processor is None:
            return "Error: BLIP model not loaded. Please check installation."
        
        try:
            # Prepare image
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            # Generate caption
            out = self.model.generate(**inputs, max_length=100)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            # Enhanced explanation with context
            if context:
                explanation = f"**Image Analysis:**\n{caption}\n\n"
                explanation += f"**Context:** This diagram relates to {context}. "
                explanation += f"The image shows: {caption}"
            else:
                explanation = f"**Diagram Explanation:**\n{caption}"
            
            return explanation
        
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def analyze_with_prompt(self, image: Image.Image, prompt: str) -> str:
        """Analyze image with custom prompt (conditional generation)."""
        if self.model is None or self.processor is None:
            return "Error: BLIP model not loaded."
        
        try:
            # Prepare inputs with text prompt
            inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
            
            # Generate
            out = self.model.generate(**inputs, max_length=150)
            response = self.processor.decode(out[0], skip_special_tokens=True)
            
            return response
        
        except Exception as e:
            return f"Error: {str(e)}"
