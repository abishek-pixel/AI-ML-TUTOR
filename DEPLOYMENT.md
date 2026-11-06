# Deployment Guide

## Prerequisites
- API key (Gemini or Groq)
- GitHub account
- Deployment platform account (Hugging Face Spaces recommended)

## Option 1: Hugging Face Spaces (Recommended) 🤗

### Step 1: Create Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in details:
   - **Name**: `ai-ml-dl-tutor` (or your choice)
   - **License**: MIT
   - **SDK**: Gradio
   - **Hardware**: CPU Basic (free)
4. Click "Create Space"

### Step 2: Upload Files
Upload these files to your Space:
```
├── app.py
├── requirements.txt
├── packages.txt
├── README.md
├── .gitignore
├── src/
│   ├── config.py
│   ├── llm_client.py
│   ├── prompt_engineer.py
│   ├── chat_manager.py
│   ├── knowledge_base.py
│   ├── image_processor.py
│   ├── content_generator.py
│   └── responsible_ai.py
├── data/
│   └── sample_notes.txt
├── models/ (empty, created at runtime)
└── outputs/ (empty, created at runtime)
```

### Step 3: Set Environment Variables
1. Go to **Settings** → **Repository secrets**
2. Add secrets:
   - Name: `GEMINI_API_KEY` (or `GROQ_API_KEY`)
   - Value: Your actual API key
   - Name: `LLM_PROVIDER`
   - Value: `gemini` (or `groq`)

### Step 4: Wait for Build
- Space will automatically build and deploy
- Check logs for any errors
- Once ready, you'll see "Running" status

### Step 5: Test Deployment
- Click "App" tab to view your live app
- Test all features:
  - Concept explanation
  - Prompt comparison
  - Chat with memory
  - Image upload
  - Content generation

### Your Live URL
```
https://huggingface.co/spaces/YOUR_USERNAME/ai-ml-dl-tutor
```

---

## Option 2: Streamlit Community Cloud ☁️

### Step 1: Prepare Repository
```bash
# Ensure code is in GitHub
git add .
git commit -m "Prepare for Streamlit deployment"
git push origin main
```

### Step 2: Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Set main file: `app.py`
5. Add secrets in "Advanced settings":
```toml
GEMINI_API_KEY = "your_key_here"
LLM_PROVIDER = "gemini"
```

### Step 3: Deploy
- Click "Deploy"
- Wait for deployment to complete
- Test your app

---

## Option 3: Local Development 💻

### Step 1: Clone and Setup
```bash
git clone <your-repo>
cd NLP_MINI_PROJECT

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your API key
notepad .env  # Windows
nano .env     # Linux/Mac
```

Add:
```env
GEMINI_API_KEY=your_actual_api_key_here
LLM_PROVIDER=gemini
```

### Step 3: Test Setup
```bash
python test_setup.py
```

All tests should pass ✓

### Step 4: Run Application
```bash
python app.py
```

Access at: `http://localhost:7860`

---

## Option 4: Docker Deployment 🐳

### Build Image
```bash
docker build -t ai-tutor .
```

### Run Container
```bash
docker run -p 7860:7860 \
  -e GEMINI_API_KEY=your_key \
  -e LLM_PROVIDER=gemini \
  ai-tutor
```

Access at: `http://localhost:7860`

---

## API Key Setup

### Get Gemini API Key (Free)
1. Go to [ai.google.dev](https://ai.google.dev)
2. Click "Get API key"
3. Create new key
4. Copy key

### Get Groq API Key (Free)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Go to API Keys
4. Create new key
5. Copy key

---

## Troubleshooting

### Issue: "API key not found"
**Solution**: Check environment variables are set correctly
```bash
# Verify .env file
cat .env

# Or check Spaces secrets are added
```

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "CUDA out of memory"
**Solution**: Models auto-detect CPU/GPU. Use CPU-only deployment:
```python
# In src/content_generator.py and src/image_processor.py
device = "cpu"  # Force CPU
```

### Issue: "Slow image generation"
**Solution**: 
- Use sd-turbo (already configured)
- Or use Hugging Face Inference API
- Or disable image generation temporarily

### Issue: "BLIP model download fails"
**Solution**: Models download on first run. Ensure:
- Internet connection stable
- Sufficient disk space (2GB+)
- Or pre-download models locally

---

## Performance Optimization

### For Free Tier Deployments

1. **Reduce Model Size**
```python
# Use smaller models
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"  # Already minimal
```

2. **Cache Results**
```python
# Add caching to Gradio functions
@gr.cache
def explain_concept(...):
    ...
```

3. **Limit Concurrent Users**
```python
# In app.py
app.queue(max_size=5)
app.launch(max_threads=2)
```

4. **Use Inference API for Heavy Models**
```python
# Instead of loading locally
from huggingface_hub import InferenceClient
client = InferenceClient()
```

---

## Monitoring

### Check Logs
**Hugging Face Spaces**: View logs in "Logs" tab

**Local**: Terminal output

**Docker**: 
```bash
docker logs <container_id>
```

### Monitor Usage
- API call count
- Response times
- Error rates

---

## Updating Deployment

### Update Hugging Face Space
```bash
# Commit changes
git add .
git commit -m "Update feature X"
git push origin main
```

Space auto-rebuilds on push.

### Update Local
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python app.py
```

---

## Security Best Practices

1. **Never commit API keys**
   - Use .gitignore
   - Use environment variables
   - Use platform secrets

2. **Validate inputs**
   - Already implemented in code
   - Length limits on text inputs

3. **Rate limiting**
   - Consider adding for production
   - Use Gradio's queue system

4. **Content filtering**
   - Already implemented (ResponsibleAI class)
   - Monitor and update filters

---

## Cost Considerations

### Free Tier Limits

**Hugging Face Spaces (Free)**
- CPU: Basic (2 vCPU, 16GB RAM)
- Storage: 50GB
- Sleep after inactivity: Yes

**Gemini API (Free)**
- 60 requests/minute
- 1500 requests/day
- No cost

**Groq API (Free)**
- High rate limits
- Free tier available
- Check current limits

### Upgrade Options
- HF Spaces: $0/month (free) → $5/month (better CPU)
- Gemini: Pay-as-you-go for higher limits
- Groq: Various tiers available

---

## Production Checklist

- [ ] API keys in environment (not code)
- [ ] All dependencies in requirements.txt
- [ ] README.md complete
- [ ] MODEL_CARD.md added
- [ ] .gitignore configured
- [ ] Test all features locally
- [ ] Deploy to platform
- [ ] Test deployed version
- [ ] Monitor for 24 hours
- [ ] Document live URL
- [ ] Create demo video
- [ ] Submit project

---

## Support

**Issues**: Create GitHub issue  
**Questions**: Check README.md  
**Updates**: Watch GitHub repo

---

**Last Updated**: November 6, 2026
