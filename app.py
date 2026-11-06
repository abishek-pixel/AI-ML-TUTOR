"""Main Gradio application for AI-ML-DL Concept Tutor."""
import gradio as gr
import os
from src.config import Config
from src.llm_client import LLMClient
from src.prompt_engineer import PromptEngineer
from src.chat_manager import ChatManager
from src.knowledge_base import KnowledgeBase
from src.image_processor import ImageProcessor
from src.content_generator import ContentGenerator
from src.responsible_ai import ResponsibleAI

# Initialize components
print("Initializing AI Tutor...")

try:
    Config.validate()
    llm_client = LLMClient()
    prompt_engineer = PromptEngineer(llm_client)
    chat_manager = ChatManager()
    knowledge_base = KnowledgeBase()
    image_processor = ImageProcessor()
    content_generator = ContentGenerator()
    responsible_ai = ResponsibleAI()
    
    # Load knowledge base
    print("Loading knowledge base...")
    knowledge_base.load_and_index_notes()
    
    print("✓ Initialization complete!")
except Exception as e:
    print(f"⚠ Initialization warning: {e}")

# Tab 1: Concept Explanation
def explain_concept(term: str, level: str, temperature: float):
    """Main explanation function with fact-checking."""
    if not term:
        return "Please enter a term to explain.", None, ""
    
    # Create prompt
    prompt = f"""Explain the AI/ML/DL concept "{term}" at {level} level.

Provide:
1. Clear explanation suitable for {level} level
2. Key components and how it works
3. Practical applications
4. Comparison table with 3 related concepts

Format the comparison as a markdown table."""
    
    # Generate response
    response = llm_client.generate(prompt, temperature)
    
    # Fact-check against knowledge base
    is_supported, supporting_docs, confidence = knowledge_base.verify_answer(response, term)
    
    # Apply responsible AI checks
    if not is_supported or confidence < Config.SIMILARITY_THRESHOLD:
        response = "**I'm not sure about this concept based on my knowledge base.** " + response
        response += f"\n\n*Confidence: {confidence:.2%} - Please verify with authoritative sources.*"
    else:
        response = responsible_ai.add_disclaimer(response, confidence)
    
    # Generate safety report
    safety_report = responsible_ai.generate_report(term, response, supporting_docs)
    
    # Show supporting documents
    sources = "\n\n".join([f"**Source {i+1}:** {doc[:200]}..." for i, doc in enumerate(supporting_docs[:3])])
    
    return response, sources, safety_report

# Tab 2: Prompt Technique Comparison
def compare_prompts(term: str, level: str, temperature: float):
    """Compare three prompt engineering techniques."""
    if not term:
        return "Please enter a term.", "", "", ""
    
    results = prompt_engineer.compare_techniques(term, level, temperature)
    
    # Format results
    zero_out = f"**Score: {results['zero_shot']['score']:.2f}**\n\n{results['zero_shot']['response']}"
    few_out = f"**Score: {results['few_shot']['score']:.2f}**\n\n{results['few_shot']['response']}"
    cot_out = f"**Score: {results['chain_of_thought']['score']:.2f}**\n\n{results['chain_of_thought']['response']}"
    
    # Create comparison table
    table = f"""| Technique | Score | Length | Structure |
|-----------|-------|--------|-----------|
| Zero-shot | {results['zero_shot']['score']:.2f} | {len(results['zero_shot']['response'])} chars | Basic |
| Few-shot | {results['few_shot']['score']:.2f} | {len(results['few_shot']['response'])} chars | With examples |
| Chain-of-thought | {results['chain_of_thought']['score']:.2f} | {len(results['chain_of_thought']['response'])} chars | Step-by-step |

**Best technique:** {max(results.keys(), key=lambda k: results[k]['score']).replace('_', ' ').title()}
"""
    
    return zero_out, few_out, cot_out, table

# Tab 3: Chat with Memory
def chat_with_memory(message: str, history, temperature: float):
    """Chat with conversation memory."""
    if not message:
        return history, None
    
    # Add user message
    chat_manager.add_message("user", message)
    
    # Create context-aware prompt
    context = chat_manager.get_context_string()
    prompt = f"""{context}

user: {message}

assistant: """
    
    # Generate response
    response = llm_client.generate(prompt, temperature, max_tokens=500)
    
    # Add assistant response
    chat_manager.add_message("assistant", response)
    
    # Generate attention heatmap
    attention_img = chat_manager.generate_attention_heatmap(message)
    
    # Update history
    history.append([message, response])
    
    return history, attention_img

def clear_chat():
    """Clear chat history."""
    chat_manager.clear_history()
    return [], None

# Tab 4: Image Explanation
def explain_image(image, context: str):
    """Explain uploaded diagram using BLIP."""
    if image is None:
        return "Please upload an image."
    
    explanation = image_processor.explain_diagram(image, context)
    return explanation

# Tab 5: Generate Content
def generate_content(concept: str, summary_text: str):
    """Generate illustration and audio summary."""
    if not concept:
        return None, None, "Please enter a concept."
    
    # Generate illustration
    illustration = content_generator.generate_concept_illustration(concept)
    
    # Generate audio
    if summary_text:
        audio_path = content_generator.generate_audio_summary(summary_text, concept)
        status = f"✓ Generated illustration and audio summary for '{concept}'"
    else:
        audio_path = None
        status = f"✓ Generated illustration for '{concept}'"
    
    return illustration, audio_path, status

# Build Gradio Interface
with gr.Blocks(title=Config.APP_TITLE, theme=gr.themes.Soft()) as app:
    gr.Markdown(f"# {Config.APP_TITLE}")
    gr.Markdown(Config.APP_DESCRIPTION)
    
    with gr.Tabs():
        # Tab 1: Main Tutor
        with gr.Tab("📚 Concept Tutor"):
            with gr.Row():
                with gr.Column():
                    term_input = gr.Textbox(label="AI/ML/DL Term", placeholder="e.g., Neural Network, Transformer, Backpropagation")
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
                        chat_input = gr.Textbox(label="Your Question", placeholder="Ask about any AI/ML/DL concept...")
                        chat_temp = gr.Slider(0.0, 1.0, value=0.7, label="Temperature", scale=1)
                    with gr.Row():
                        chat_btn = gr.Button("Send", variant="primary")
                        clear_btn = gr.Button("Clear History")
                
                with gr.Column(scale=1):
                    attention_plot = gr.Image(label="Attention Heatmap", type="pil")
            
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
                    image_context = gr.Textbox(label="Context (optional)", placeholder="e.g., Neural Network architecture")
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
                    gen_summary = gr.Textbox(label="Summary Text for Audio", lines=5, placeholder="Enter text to convert to audio...")
                    gen_btn = gr.Button("Generate", variant="primary")
                
                with gr.Column():
                    gen_image = gr.Image(label="Generated Illustration", type="pil")
                    gen_audio = gr.Audio(label="Audio Summary")
                    gen_status = gr.Markdown()
            
            gen_btn.click(
                generate_content,
                inputs=[gen_concept, gen_summary],
                outputs=[gen_image, gen_audio, gen_status]
            )
    
    gr.Markdown("""
    ---
    **Instructions:**
    - **Concept Tutor:** Get explanations at different levels with fact-checking
    - **Prompt Techniques:** Compare zero-shot, few-shot, and chain-of-thought approaches
    - **Chat:** Have conversations with memory and see attention patterns
    - **Diagram:** Upload AI/ML/DL diagrams for BLIP-powered explanations
    - **Generate:** Create concept illustrations and audio summaries
    
    *Note: Requires API key (Gemini/Groq) in environment or Spaces secrets*
    """)

if __name__ == "__main__":
    app.launch(share=False)
