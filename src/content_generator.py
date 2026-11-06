"""Content generation: images (diffusion) and audio (TTS)."""
import os
import torch
from PIL import Image
from diffusers import AutoPipelineForText2Image
from gtts import gTTS
from src.config import Config

class ContentGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.image_pipeline = None
        self._load_models()
    
    def _load_models(self):
        """Load generative models lazily."""
        try:
            print(f"Loading diffusion model on {self.device}...")
            self.image_pipeline = AutoPipelineForText2Image.from_pretrained(
                Config.DIFFUSION_MODEL,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.image_pipeline = self.image_pipeline.to(self.device)
            print("Diffusion model loaded")
        except Exception as e:
            print(f"Warning: Could not load diffusion model: {e}")
            self.image_pipeline = None
    
    def generate_concept_illustration(self, concept: str, style: str = "educational diagram") -> Image.Image:
        """Generate illustration for a concept using diffusion model."""
        if self.image_pipeline is None:
            # Return placeholder image
            return self._create_placeholder_image(concept)
        
        try:
            # Create prompt
            prompt = f"A clear {style} illustrating {concept}, simple, educational, high quality"
            
            # Generate image
            result = self.image_pipeline(
                prompt=prompt,
                num_inference_steps=4,  # Fast generation with sd-turbo
                guidance_scale=0.0
            )
            
            image = result.images[0]
            
            # Save
            output_path = os.path.join(Config.OUTPUTS_DIR, f"{concept.replace(' ', '_')}_illustration.png")
            os.makedirs(Config.OUTPUTS_DIR, exist_ok=True)
            image.save(output_path)
            
            return image
        
        except Exception as e:
            print(f"Error generating image: {e}")
            return self._create_placeholder_image(concept)
    
    def _create_placeholder_image(self, text: str) -> Image.Image:
        """Create a simple placeholder image."""
        from PIL import ImageDraw, ImageFont
        
        img = Image.new('RGB', (512, 512), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add text
        text_lines = [
            "Concept Illustration",
            text[:50],
            "",
            "(Image generation unavailable)",
            "Using placeholder"
        ]
        
        y_pos = 200
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line)
            width = bbox[2] - bbox[0]
            draw.text((256 - width // 2, y_pos), line, fill='darkblue')
            y_pos += 30
        
        return img
    
    def generate_audio_summary(self, text: str, concept: str) -> str:
        """Generate audio summary using TTS."""
        try:
            # Create concise summary (first 500 chars)
            summary = text[:500] + ("..." if len(text) > 500 else "")
            
            # Generate audio
            tts = gTTS(text=summary, lang='en', slow=False)
            
            # Save
            output_path = os.path.join(Config.OUTPUTS_DIR, f"{concept.replace(' ', '_')}_summary.mp3")
            os.makedirs(Config.OUTPUTS_DIR, exist_ok=True)
            tts.save(output_path)
            
            return output_path
        
        except Exception as e:
            return f"Error generating audio: {str(e)}"
