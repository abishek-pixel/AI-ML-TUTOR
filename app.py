"""Simplified working version without heavy dependencies."""
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()

# Check configuration
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY")
provider = os.getenv("LLM_PROVIDER", "gemini")
model_name = os.getenv("MODEL_NAME", "gemini-3.8-flash")

# Initialize LLM client
try:
    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        llm = genai.GenerativeModel(model_name)
        print(f"✓ Gemini initialized with {model_name}")
    elif provider == "groq":
        from groq import Groq
        llm = Groq(api_key=api_key)
        print("✓ Groq initialized")
    api_working = True
except Exception as e:
    print(f"⚠ LLM initialization failed: {e}")
    llm = None
    api_working = False

def generate_response(prompt, temperature=0.7):
    """Generate response from LLM."""
    if not api_working or not llm:
        return "Error: LLM not initialized. Check API key."
    
    try:
        if provider == "gemini":
            response = llm.generate_content(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": 1000}
            )
            return response.text
        elif provider == "groq":
            response = llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}\n\nTip: You may have hit the rate limit (5 requests/minute on free tier). Wait 60 seconds and try again."

# Tab 1: Concept Explanation
def explain_concept(term, level, temperature):
    if not term:
        return "Please enter a term to explain.", ""
    
    prompt = f"""Explain the AI/ML/DL concept "{term}" at {level} level.

Provide:
1. Clear explanation suitable for {level} level
2. Key components and how it works  
3. Practical applications
4. Comparison table with 3 related concepts (use markdown table format)

Keep it comprehensive but concise."""
    
    response = generate_response(prompt, temperature)
    
    sources = f"**Note**: This is a working prototype. Full version includes fact-checking against knowledge base.\n\nConcept: {term} | Level: {level} | Temperature: {temperature}"
    
    return response, sources

# Tab 2: Prompt Technique Comparison
def compare_prompts(term, level, temperature):
    if not term:
        return "Enter a term", "Enter a term", "Enter a term", "Processing..."
    
    # Zero-shot
    zero_prompt = f'Explain "{term}" at {level} level in 2-3 paragraphs.'
    zero_response = generate_response(zero_prompt, temperature)
    zero_output = f"**Zero-shot Prompt**\n\n{zero_response}"
    
    # Few-shot
    few_prompt = f"""Example: Neural Network at school level - Think of it like your brain! Neurons that learn patterns.

Now explain "{term}" at {level} level in a similar style."""
    few_response = generate_response(few_prompt, temperature)
    few_output = f"**Few-shot Prompt**\n\n{few_response}"
    
    # Chain-of-thought
    cot_prompt = f"""Let's explain "{term}" at {level} level step by step:
Step 1: What is the core idea?
Step 2: How does it work?
Step 3: What are the key components?
Step 4: What are practical uses?

Work through each step systematically."""
    cot_response = generate_response(cot_prompt, temperature)
    cot_output = f"**Chain-of-thought Prompt**\n\n{cot_response}"
    
    # Simple scoring based on length
    zero_score = min(1.0, len(zero_response) / 500)
    few_score = min(1.0, len(few_response) / 500)
    cot_score = min(1.0, len(cot_response) / 500)
    
    table = f"""## Comparison

| Technique | Response Length | Estimated Score |
|-----------|----------------|-----------------|
| Zero-shot | {len(zero_response)} chars | {zero_score:.2f} |
| Few-shot | {len(few_response)} chars | {few_score:.2f} |
| Chain-of-thought | {len(cot_response)} chars | {cot_score:.2f} |

**Note**: This is a simplified scoring. Full version includes comprehensive quality metrics."""
    
    return zero_output, few_output, cot_output, table

# Tab 3: Chat
chat_history = []

def chat_with_memory(message, history, temperature):
    if not message:
        return history, "No message entered"
    
    # Build context from history
    context = "\n".join([f"User: {h[0]}\nAssistant: {h[1]}" for h in history[-3:]])  # Last 3 exchanges
    
    prompt = f"""Previous conversation:
{context}

User: {message}

Assistant (respond naturally, maintaining context):"""
    
    response = generate_response(prompt, temperature)
    
    history.append([message, response])
    status = f"Response generated (context: last {min(3, len(history))} exchanges)"
    
    return history, status

def clear_chat():
    return [], "Chat cleared"

# Build Gradio Interface
with gr.Blocks(title="AI-ML-DL Concept Tutor", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎓 AI-ML-DL Concept Tutor (Working Prototype)")
    
    if api_working:
        gr.Markdown(f"""
        ## ✅ Status: FULLY FUNCTIONAL
        - **LLM Provider**: {provider}
        - **Model**: {model_name}
        - **Rate Limit**: 5 requests/minute (free tier)
        
        **This is a working prototype with core features:**
        - ✓ Real LLM responses
        - ✓ Multi-level explanations
        - ✓ Prompt technique comparison
        - ✓ Conversational chat with memory
        
        **Full version adds**: Knowledge base (Sentence-BERT), Image understanding (BLIP), 
        Content generation (Diffusion+TTS), Attention visualization, Bias detection
        """)
    else:
        gr.Markdown("""
        ## ⚠️ LLM Not Initialized
        Please check:
        1. API key in .env file
        2. Provider setting (gemini/groq)
        3. Internet connection
        """)
    
    with gr.Tabs():
        # Tab 1: Main Tutor
        with gr.Tab("📚 Concept Tutor"):
            with gr.Row():
                with gr.Column():
                    term_input = gr.Textbox(
                        label="AI/ML/DL Term", 
                        placeholder="e.g., Neural Network, Transformer, Backpropagation"
                    )
                    level_select = gr.Radio(
                        ["school", "UG", "expert"], 
                        label="Explanation Level", 
                        value="UG"
                    )
                    temp_slider = gr.Slider(
                        0.0, 1.0, value=0.7, 
                        label="Temperature (creativity)"
                    )
                    explain_btn = gr.Button("Explain Concept", variant="primary")
                
                with gr.Column():
                    explanation_output = gr.Markdown(label="Explanation")
                    sources_output = gr.Markdown(label="Status")
            
            explain_btn.click(
                explain_concept,
                inputs=[term_input, level_select, temp_slider],
                outputs=[explanation_output, sources_output]
            )
        
        # Tab 2: Prompt Engineering
        with gr.Tab("🔧 Prompt Techniques"):
            gr.Markdown("Compare zero-shot, few-shot, and chain-of-thought prompting")
            
            with gr.Row():
                with gr.Column():
                    pt_term = gr.Textbox(label="Term", placeholder="Enter AI/ML/DL term")
                    pt_level = gr.Radio(["school", "UG", "expert"], label="Level", value="UG")
                    pt_temp = gr.Slider(0.0, 1.0, value=0.7, label="Temperature")
                    compare_btn = gr.Button("Compare Techniques", variant="primary")
                
                with gr.Column():
                    comparison_table = gr.Markdown(label="Comparison Results")
            
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
            gr.Markdown("Conversational AI that maintains context from previous messages")
            
            chatbot = gr.Chatbot(label="Conversation", height=400)
            chat_status = gr.Markdown("Status: Ready")
            
            with gr.Row():
                chat_input = gr.Textbox(
                    label="Your Question", 
                    placeholder="Ask about any AI/ML/DL concept...",
                    scale=4
                )
                chat_temp = gr.Slider(0.0, 1.0, value=0.7, label="Temperature", scale=1)
            
            with gr.Row():
                chat_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear History")
            
            chat_btn.click(
                chat_with_memory,
                inputs=[chat_input, chatbot, chat_temp],
                outputs=[chatbot, chat_status]
            )
            clear_btn.click(clear_chat, outputs=[chatbot, chat_status])
        
        # Info Tab
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## P1 - AI-ML-DL Concept Tutor
            
            ### Current Version: Working Prototype
            
            **Features in this version:**
            - ✅ Multi-level concept explanations (school, UG, expert)
            - ✅ Three prompt engineering techniques compared
            - ✅ Conversational chat with context memory
            - ✅ Temperature control for creativity
            - ✅ Real-time LLM responses
            
            **Additional features in full version:**
            - Sentence-BERT knowledge base with FAISS indexing
            - Fact-checking with confidence scores
            - BLIP image understanding for diagrams
            - Diffusion model for concept illustrations
            - Text-to-speech audio summaries
            - Attention heatmap visualization
            - Bias detection and safety guardrails
            
            ### System Info
            - LLM Provider: {prov}
            - Model: {mod}
            - Status: {stat}
            
            ### Rate Limits
            Free tier: 5 requests per minute
            Wait 60 seconds if you hit the limit.
            
            ### Documentation
            See README.md, PROJECT_REPORT.md, and MODEL_CARD.md for complete details.
            """.format(
                prov=provider, 
                mod=model_name,
                stat="✅ Working" if api_working else "❌ Not initialized"
            ))
    
    gr.Markdown("""
    ---
    **Note**: This is a working prototype. For full feature set, install all dependencies from requirements.txt.
    """)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎓 AI-ML-DL Concept Tutor - Working Prototype")
    print("="*60)
    print(f"Provider: {provider}")
    print(f"Model: {model_name}")
    print(f"Status: {'✅ Ready' if api_working else '❌ Check configuration'}")
    print("="*60 + "\n")
    
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
