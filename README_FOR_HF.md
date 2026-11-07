---
title: AI-ML-DL Concept Tutor
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.13.0
app_file: app.py
pinned: false
---

# AI-ML-DL Concept Tutor 🎓

An intelligent tutoring system that explains AI, Machine Learning, and Deep Learning concepts at multiple proficiency levels (school, undergraduate, expert).

## Features

### 🎯 Multi-Level Explanations
- **School Level**: Simple analogies and everyday language
- **UG Level**: Technical terms with formulas
- **Expert Level**: Mathematical notation and research depth

### 🔧 Prompt Engineering
Compare three advanced techniques:
- **Zero-shot**: Direct instruction without examples
- **Few-shot**: Learning from provided examples  
- **Chain-of-thought**: Step-by-step reasoning

### 💬 Conversational Chat
- Maintains conversation context
- Natural follow-up questions
- Memory of last exchanges

## How to Use

1. **Concept Tutor Tab**: 
   - Enter any AI/ML/DL term (e.g., "Neural Network", "Transformer")
   - Select your proficiency level
   - Adjust temperature for creativity
   - Get comprehensive explanations

2. **Prompt Techniques Tab**:
   - Compare different prompting strategies
   - See which technique works best
   - Learn advanced prompt engineering

3. **Chat Tab**:
   - Ask questions naturally
   - Follow up with related queries
   - Explore concepts in depth

## Technology Stack

- **LLM**: Google Gemini (gemini-3.8-flash)
- **UI**: Gradio
- **Language**: Python

## Example Queries

- "Explain backpropagation at UG level"
- "What is attention mechanism in transformers?"
- "Compare CNN and RNN for image processing"

## Project Information

**Course**: NLP Mini Project  
**Project Code**: P1 - AI-ML-DL Concept Tutor  
**Features**: Multi-level adaptation, Prompt engineering, Conversational AI

## Rate Limits

This app uses Gemini API free tier:
- 5 requests per minute
- If you hit the limit, wait 60 seconds

## Responsible AI

- Fact-checking against knowledge base
- Confidence scoring
- Appropriate disclaimers for low-confidence responses

---

**Note**: This is a working prototype demonstrating core NLP capabilities including prompt engineering, conversational memory, and multi-level text generation.
