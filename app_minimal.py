"""Minimal version to test Gradio UI without heavy dependencies."""
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()

# Check if API key exists
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY")
provider = os.getenv("LLM_PROVIDER", "gemini")

if not api_key:
    print("⚠️  WARNING: No API key found in .env file")
    print("Please add your API key to the .env file:")
    print("  GEMINI_API_KEY=your_key_here")
    print("  LLM_PROVIDER=gemini")
    print("\nRunning in demo mode with placeholder responses...\n")

# Demo functions (placeholders until full dependencies installed)
def explain_concept(term, level, temperature):
    if not term:
        return "Please enter a term to explain.", "", ""
    
    if not api_key:
        explanation = f"""**DEMO MODE** (Add API key to .env for real responses)

### {term} at {level} Level

This is a placeholder response. The actual system will:
- Use advanced prompt engineering (zero-shot, few-shot, chain-of-thought)
- Generate explanations adapted to {level} level
- Include comparison tables with related concepts
- Fact-check against the knowledge base
- Provide confidence scores

Temperature: {temperature}"""
        
        sources = "Knowledge base not yet loaded. Will show supporting sources here."
        report = f"**Safety Report**: Bias: 0.0, Confidence: N/A (demo mode)"
        return explanation, sources, report
    
    # If API key exists, show instructions
    return (
        f"API key detected! Install full dependencies to use:\n\n`pip install -r requirements.txt`\n\nThen run: `python app.py`",
        "Full knowledge base will be loaded",
        "Responsible AI checks will run"
    )

def compare_prompts(term, level, temperature):
    if not term:
        return "Enter a term", "Enter a term", "Enter a term", "Enter a term"
    
    zero = f"**Zero-shot** (Score: 0.75)\nDirect explanation of {term} at {level} level..."
    few = f"**Few-shot** (Score: 0.82)\nWith examples: {term} at {level} level..."
    cot = f"**Chain-of-thought** (Score: 0.88)\nStep-by-step: {term} at {level} level..."
    
    table = f"""| Technique | Score | Status |
|-----------|-------|--------|
| Zero-shot | 0.75 | Demo |
| Few-shot | 0.82 | Demo |
| Chain-of-thought | 0.88 | **Winner** |

Install full dependencies for real comparisons!"""
    
    return zero, few, cot, table

def chat_with_memory(message, history, temperature):
    if not message:
        return history, None
    
    response = f"[DEMO] Response to: {message}\n\nInstall full dependencies for real chat with memory and attention heatmap."
    history.append([message, response])
    return history, None

def clear_chat():
    return [], None

def explain_image(image, context):
    if image is None:
        return "Please upload an image."
    return "**DEMO MODE**: BLIP model will analyze uploaded diagrams once dependencies are installed."

def generate_content(concept, summary_text):
    if not concept:
        return None, None, "Please enter a concept."
    
    status = f"**DEMO MODE**: Will generate illustration and audio for '{concept}' with full installation."
    return None, None, status

# Build Gradio Interface
with gr.Blocks(title="AI-ML-DL Concept Tutor", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎓 AI-ML-DL Concept Tutor")
    
    if not api_key:
        gr.Markdown("""
        ## ⚠️ Demo Mode
        **Add your API key to `.env` file to enable full functionality:**
        1. Get free API key from [Google AI Studio](https://ai.google.dev)
        2. Edit `.env` file: `GEMINI_API_KEY=your_key_here`
        3. Install full dependencies: `pip install -r requirements.txt`
        4. Run full app: `python app.py`
        
        **This demo shows the UI structure without backend processing.**
        """)
    else:
        gr.Markdown("""
        ## ✅ API Key Detected!
        **Next steps:**
        1. Install full dependencies: `pip install -r requirements.txt`
        2. Run full app: `python app.py`
        
        **This is a minimal UI test. The full app has all features working.**
        """)
    
    gr.Markdown("Multi-level AI/ML/DL concept explanations with prompt engineering, RAG, and multimodal understanding")
    
    with gr.Tabs():
        # Tab 1: Main Tutor
        with gr.Tab("📚 Concept Tutor"):
            with gr.Row():
                with gr.Column():
                    term_input = gr.Textbox(label="AI/ML/DL Term", placeholder="e.g., Neural Network, Transformer")
                    level_select = gr.Radio(["school", "UG", "expert"], label="Explanation Level", value="UG")
                    temp_slider = gr.Slider(0.0, 1.0, value=0.7, label="Temperature (creativity)")
                    explain_btn = gr.Button("Explain Concept", variant="primary")
                
                with gr.Column():
                    explanation_output = gr.Markdown(label="Explanation")
                    sources_output = gr.Markdown(label="Supporting Sources")
            
            with gr.Accordion("Responsible AI Report", open=False):
                safety_output = gr.Markdown()
            
            explain_btn.click(
                explain_concept,
                inputs=[term_input, level_select, temp_slider],
                outputs=[explanation_output, sources_output, safety_output]
            )
        
        # Tab 2: Prompt Engineering
        with gr.Tab("🔧 Prompt Techniques"):
            with gr.Row():
                with gr.Column():
                    pt_term = gr.Textbox(label="Term", placeholder="Enter AI/ML/DL term")
                    pt_level = gr.Radio(["school", "UG", "expert"], label="Level", value="UG")
                    pt_temp = gr.Slider(0.0, 1.0, value=0.7, label="Temperature")
                    compare_btn = gr.Button("Compare Techniques", variant="primary")
                
                with gr.Column():
                    comparison_table = gr.Markdown(label="Comparison Table")
            
            with gr.Row():
                zero_shot_out = gr.Markdown(label="Zero-shot")
                few_shot_out = gr.Markdown(label="Few-shot")
                cot_out = gr.Markdown(label="Chain-of-thought")
            
            compare_btn.click(
                compare_prompts,
                inputs=[pt_term, pt_level, pt_temp],
                outputs=[zero_shot_out, few_shot_out, cot_out, comparison_table]
            )
        
        # Tab 3: Chat
        with gr.Tab("💬 Chat with Memory"):
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(label="Conversation", height=400)
                    with gr.Row():
                        chat_input = gr.Textbox(label="Your Question", placeholder="Ask about AI/ML/DL...")
                        chat_temp = gr.Slider(0.0, 1.0, value=0.7, label="Temperature", scale=1)
                    with gr.Row():
                        chat_btn = gr.Button("Send", variant="primary")
                        clear_btn = gr.Button("Clear History")
                
                with gr.Column(scale=1):
                    attention_plot = gr.Image(label="Attention Heatmap (full version)", type="pil")
            
            chat_btn.click(
                chat_with_memory,
                inputs=[chat_input, chatbot, chat_temp],
                outputs=[chatbot, attention_plot]
            )
            clear_btn.click(clear_chat, outputs=[chatbot, attention_plot])
        
        # Tab 4: Image Analysis
        with gr.Tab("🖼️ Diagram Explanation"):
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(label="Upload Diagram", type="pil")
                    image_context = gr.Textbox(label="Context (optional)", placeholder="e.g., Neural Network")
                    image_btn = gr.Button("Explain Diagram", variant="primary")
                
                with gr.Column():
                    image_explanation = gr.Markdown(label="Explanation")
            
            image_btn.click(
                explain_image,
                inputs=[image_input, image_context],
                outputs=image_explanation
            )
        
        # Tab 5: Content Generation
        with gr.Tab("🎨 Generate Content"):
            with gr.Row():
                with gr.Column():
                    gen_concept = gr.Textbox(label="Concept", placeholder="e.g., Neural Network")
                    gen_summary = gr.Textbox(label="Summary Text", lines=5)
                    gen_btn = gr.Button("Generate", variant="primary")
                
                with gr.Column():
                    gen_image = gr.Image(label="Generated Illustration (full version)", type="pil")
                    gen_audio = gr.Audio(label="Audio Summary (full version)")
                    gen_status = gr.Markdown()
            
            gen_btn.click(
                generate_content,
                inputs=[gen_concept, gen_summary],
                outputs=[gen_image, gen_audio, gen_status]
            )
    
    gr.Markdown("""
    ---
    ### 📋 Installation Status
    
    **Current**: Minimal UI test (Gradio only)
    
    **For full functionality:**
    ```bash
    pip install -r requirements.txt
    python app.py
    ```
    
    **Features in full version:**
    - ✓ Real LLM responses (Gemini/Groq)
    - ✓ Sentence-BERT knowledge base
    - ✓ BLIP image understanding
    - ✓ Diffusion model illustrations
    - ✓ Text-to-speech audio
    - ✓ Attention heatmaps
    - ✓ Fact-checking & bias detection
    """)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎓 AI-ML-DL Concept Tutor - Minimal UI Test")
    print("="*60)
    
    if api_key:
        print(f"✓ API key detected for {provider}")
        print("\n📦 Next: Install full dependencies")
        print("   pip install -r requirements.txt")
    else:
        print("⚠️  No API key found in .env")
        print("\n📝 Add your API key:")
        print("   1. Edit .env file")
        print("   2. Add: GEMINI_API_KEY=your_key_here")
        print("   3. Install dependencies: pip install -r requirements.txt")
    
    print("\n🚀 Starting UI test...")
    print("="*60 + "\n")
    
    app.launch(share=False)
