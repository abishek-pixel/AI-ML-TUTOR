# Quick Start Guide

Get the AI-ML-DL Concept Tutor running in 5 minutes!

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection
- API key (Gemini or Groq)

## Step 1: Get API Key (2 minutes)

### Option A: Gemini (Recommended - Free)
1. Visit [https://ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Sign in with Google account
4. Create new key
5. Copy the key (starts with `AIzaSy...`)

### Option B: Groq (Alternative - Free)
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Go to "API Keys"
4. Create new key
5. Copy the key

## Step 2: Install (1 minute)

```bash
# Clone or download the project
cd NLP_MINI_PROJECT

# Install dependencies
pip install -r requirements.txt
```

**Note**: Installation may take 2-3 minutes depending on internet speed.

## Step 3: Configure (30 seconds)

### Windows
```powershell
# Copy example environment file
Copy-Item .env.example .env

# Edit with notepad
notepad .env
```

### Linux/Mac
```bash
# Copy example environment file
cp .env.example .env

# Edit with nano or vim
nano .env
```

### Add your API key:
```env
# For Gemini
GEMINI_API_KEY=your_actual_key_here
LLM_PROVIDER=gemini

# OR for Groq
GROQ_API_KEY=your_actual_key_here
LLM_PROVIDER=groq
```

Save and close the file.

## Step 4: Test Setup (30 seconds)

```bash
python test_setup.py
```

You should see:
```
✓ All imports successful!
✓ Config loaded
✓ API key found
✓ Sample notes found
✓ Notes indexed
✓ All tests passed!
```

## Step 5: Run Application (30 seconds)

```bash
python app.py
```

Output:
```
Initializing AI Tutor...
Loading knowledge base...
Indexed 45 document chunks
✓ Initialization complete!
Running on local URL:  http://127.0.0.1:7860
```

## Step 6: Use the App! 🎉

Open your browser and go to: **http://localhost:7860**

### Try These Examples:

**Tab 1: Concept Tutor**
1. Enter "Neural Network"
2. Select "UG" level
3. Click "Explain Concept"

**Tab 2: Prompt Techniques**
1. Enter "Transformer"
2. Click "Compare Techniques"
3. See the scores for each method

**Tab 3: Chat**
1. Type "What is backpropagation?"
2. Then "How is it used in training?"
3. Watch the attention heatmap update

**Tab 4: Image Explanation**
1. Upload any AI/ML diagram (neural network, architecture, etc.)
2. Click "Explain Diagram"

**Tab 5: Generate Content**
1. Enter "Convolutional Neural Network"
2. Add summary text
3. Click "Generate" to see illustration and audio

---

## Troubleshooting

### "API key not found"
- Check `.env` file exists
- Verify API key is pasted correctly (no extra spaces)
- Make sure you're using the right provider name

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "Connection error"
- Check internet connection
- Verify API key is valid
- Try the other LLM provider

### "Slow response"
- Normal on first run (models downloading)
- Subsequent runs will be faster
- Image generation takes 10-30 seconds

### "Port already in use"
Change port in app.py:
```python
app.launch(server_port=7861)
```

---

## What's Next?

### Deploy to Web (Optional)
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions:
- Hugging Face Spaces (recommended)
- Streamlit Community Cloud
- Docker deployment

### Customize
- Add more concepts to `data/sample_notes.txt`
- Adjust temperature and parameters in UI
- Modify prompts in `src/prompt_engineer.py`

### Test Thoroughly
```bash
python test_examples.py
```

### Read Documentation
- [README.md](README.md) - Full features and usage
- [MODEL_CARD.md](MODEL_CARD.md) - Model details and ethics
- [PROJECT_REPORT.md](PROJECT_REPORT.md) - Complete technical report

---

## Common Commands

```bash
# Run application
python app.py

# Test setup
python test_setup.py

# Generate test outputs
python test_examples.py

# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

## Getting Help

1. **Check logs**: Terminal shows errors and warnings
2. **Read README**: Comprehensive documentation
3. **Review code**: Well-commented source files
4. **Test modules**: Each component is testable individually

---

## Success Checklist

- [x] Python 3.8+ installed
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] API key obtained (Gemini or Groq)
- [x] `.env` file configured
- [x] Test passed (`python test_setup.py`)
- [x] App running (`python app.py`)
- [x] Browser open at localhost:7860
- [x] Features tested and working

**Congratulations! Your AI-ML-DL Concept Tutor is ready! 🎓🤖**

---

**Estimated Total Time**: 5-10 minutes  
**Last Updated**: November 6, 2026
