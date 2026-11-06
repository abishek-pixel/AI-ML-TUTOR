# Deployment Checklist for Hugging Face Spaces

Follow these steps to deploy your AI-ML-DL Concept Tutor to Hugging Face Spaces.

## Pre-Deployment Checklist

- [ ] All code is working locally (`python app.py` runs successfully)
- [ ] API key is configured in `.env` file
- [ ] All tests pass (`python test_setup.py`)
- [ ] `.gitignore` is properly configured (API keys not committed)
- [ ] README.md is complete and informative
- [ ] MODEL_CARD.md is included

## Step-by-Step Deployment

### Step 1: Create Hugging Face Account
1. Go to [https://huggingface.co](https://huggingface.co)
2. Sign up for a free account (if you don't have one)
3. Verify your email address

### Step 2: Create a New Space
1. Click on your profile → "New Space"
2. Fill in the details:
   - **Owner**: Your username
   - **Space name**: `ai-ml-dl-tutor` (or your choice)
   - **License**: MIT
   - **Select the Space SDK**: Gradio
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public
3. Click "Create Space"

### Step 3: Initialize Git Repository (if not already done)
```bash
# In your project directory
git init
git add .
git commit -m "Initial commit: AI-ML-DL Concept Tutor"
```

### Step 4: Push to Hugging Face Spaces
```bash
# Add Hugging Face remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/ai-ml-dl-tutor

# Push to Hugging Face
git push --force space main
```

**Note**: Replace `YOUR_USERNAME` with your actual Hugging Face username.

### Step 5: Configure Secrets (CRITICAL)
1. In your Space, go to **Settings** tab
2. Scroll to **Repository secrets**
3. Click "New secret"
4. Add the following secrets:

**Secret 1:**
- Name: `GEMINI_API_KEY` (or `GROQ_API_KEY`)
- Value: Your actual API key

**Secret 2:**
- Name: `LLM_PROVIDER`
- Value: `gemini` (or `groq`)

5. Click "Add secret" for each

### Step 6: Wait for Build
1. Go to the **App** tab
2. Watch the build logs
3. Wait for "Running" status (may take 3-5 minutes)
4. The app will appear once ready

### Step 7: Test Deployed Application
Test all features:
- [ ] Concept explanation works
- [ ] Prompt comparison generates results
- [ ] Chat responds correctly
- [ ] Image upload works (use a sample diagram)
- [ ] Content generation produces output

### Step 8: Update README with Live URL
1. Copy your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/ai-ml-dl-tutor`
2. Update README.md with the live URL
3. Commit and push:
```bash
git add README.md
git commit -m "Add live deployment URL"
git push space main
```

## Verification Checklist

After deployment, verify:
- [ ] App loads without errors
- [ ] All 5 tabs are visible
- [ ] API calls work (test concept explanation)
- [ ] No secrets are exposed in code or logs
- [ ] README displays correctly on Space page
- [ ] Model card is accessible

## Common Deployment Issues

### Issue 1: "Application Error"
**Solution**: Check build logs for missing dependencies
```bash
# Ensure all dependencies in requirements.txt
# Check packages.txt for system packages
```

### Issue 2: "API Key Not Found"
**Solution**: Verify secrets are set correctly
- Secret names must match exactly (case-sensitive)
- No extra spaces in secret values
- Use correct provider name

### Issue 3: "Out of Memory"
**Solution**: Reduce model sizes or use Inference API
- Comment out heavy models (diffusion, BLIP) for initial test
- Enable lazy loading
- Consider upgrading to CPU upgrade ($5/month)

### Issue 4: "Build Timeout"
**Solution**: Large dependencies may timeout
- Split requirements into smaller chunks
- Use pre-built wheels where available
- Consider Docker deployment for full control

### Issue 5: "Models Not Loading"
**Solution**: First run downloads models (slow)
- Be patient (can take 5-10 minutes)
- Models cache for subsequent runs
- Check logs for download progress

## Alternative: Git via Web Interface

If you prefer not to use command line:

1. **Create files manually on HF Space**:
   - Click "Files" → "Add file"
   - Upload each file from your local project
   - Commit each file

2. **Configure secrets** as in Step 5 above

3. **Build will start automatically**

## Post-Deployment

### Update Project Documentation
Update these files with your live URL:
- [ ] README.md (replace `[Your Space URL]` with actual URL)
- [ ] PROJECT_REPORT.md (add deployment section)
- [ ] DEMO_SCRIPT.md (update for demo)

### Share Your Project
- [ ] Add Space URL to project submission
- [ ] Test with different browsers
- [ ] Share with peers for feedback
- [ ] Monitor usage and logs

### Monitor Performance
Check Space settings for:
- Build logs
- Runtime logs
- Usage statistics
- User feedback

## Troubleshooting Resources

1. **Hugging Face Docs**: [https://huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
2. **Gradio Docs**: [https://gradio.app/docs/](https://gradio.app/docs/)
3. **Community Forum**: [https://discuss.huggingface.co/](https://discuss.huggingface.co/)

## Success Criteria

Your deployment is successful when:
- ✓ Space shows "Running" status
- ✓ App loads at public URL
- ✓ All features work as in local testing
- ✓ No errors in logs
- ✓ API calls return responses
- ✓ README displays on Space page

---

## Quick Deploy Commands

```bash
# One-time setup
git init
git add .
git commit -m "Initial commit"
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/ai-ml-dl-tutor

# Deploy
git push --force space main

# Update after changes
git add .
git commit -m "Update: description of changes"
git push space main
```

---

## Cost Considerations

**Free Tier** (CPU Basic):
- ✓ Sufficient for this project
- ✓ 2 vCPU, 16GB RAM
- ✓ 50GB storage
- ⚠ Sleeps after inactivity (wakes on access)

**Paid Upgrade** ($5/month - optional):
- Better CPU
- No sleep
- Faster model loading
- Higher concurrent users

For this academic project, **free tier is recommended**.

---

**Last Updated**: November 6, 2026  
**Estimated Time**: 15-20 minutes (first time)  
**Difficulty**: Beginner-friendly
