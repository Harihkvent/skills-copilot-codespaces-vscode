# Krutrim AI Setup Guide

Astra uses **Krutrim Cloud** as its primary LLM provider. Krutrim is India's first multilingual AI platform built by Ola.

## 🚀 Quick Setup

### 1. Get Your API Key

1. Visit **https://cloud.olakrutrim.com/**
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the API key (you'll need it in the next step)

### 2. Configure Astra

Add your API key to the `.env` file:

```bash
# Open .env file
nano .env

# Update these lines:
LLM_PROVIDER=krutrim
KRUTRIM_API_KEY=your-actual-api-key-here
KRUTRIM_API_URL=https://cloud.olakrutrim.com/v1
```

### 3. Restart Services

```bash
docker-compose restart
```

That's it! Astra is now powered by Krutrim AI.

## 🌟 Why Krutrim?

### Advantages

- **🇮🇳 Made in India**: Built specifically for Indian languages and context
- **🗣️ Multilingual**: Supports 10 Indian languages natively
- **☁️ Cloud-based**: No local GPU required
- **🚀 Fast**: Low latency responses
- **🔒 Secure**: Enterprise-grade security
- **💰 Cost-effective**: Competitive pricing

### Supported Languages

Krutrim understands and responds in:
- Hindi (हिंदी)
- English
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Malayalam (മലയാളം)
- Kannada (ಕನ್ನಡ)
- Marathi (मराठी)
- Bengali (বাংলা)
- Gujarati (ગુજરાતી)
- Odia (ଓଡ଼ିଆ)

## 🔧 Model Information

**Current Model**: `Krutrim-spectre-v2`

This is Krutrim's latest production model optimized for:
- Conversational AI
- Function calling
- Multi-turn dialogues
- Indian context understanding

## 📊 API Limits

Check your current plan at: https://cloud.olakrutrim.com/usage

**Free Tier** (typical):
- 10,000 tokens/day
- 1,000 requests/day
- Standard priority

**Paid Plans**:
- Higher rate limits
- Priority support
- Advanced features

## 🔄 Alternative: Use Local LLM (Ollama)

If you prefer to run AI locally without cloud dependency:

### 1. Uncomment Ollama in docker-compose.yml

```yaml
  ollama:
    image: ollama/ollama:latest
    container_name: astra-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 2. Update .env

```bash
LLM_PROVIDER=local
LOCAL_LLM_MODEL=llama2
LOCAL_LLM_URL=http://ollama:11434
```

### 3. Restart and download model

```bash
docker-compose down
docker-compose up -d
docker exec -it astra-ollama ollama pull llama2
```

**Note**: Local LLM requires:
- ~4GB disk space per model
- More RAM (8GB+ recommended)
- Slower responses compared to cloud

## 🐛 Troubleshooting

### Error: "KRUTRIM_API_KEY not configured"

**Solution**: Make sure you've added your API key to `.env`:
```bash
KRUTRIM_API_KEY=your-actual-key-here
```

### Error: "401 Unauthorized"

**Solution**: Your API key is invalid or expired
- Check if you copied the complete key
- Regenerate a new key from cloud.olakrutrim.com
- Make sure there are no extra spaces

### Error: "429 Too Many Requests"

**Solution**: You've hit rate limits
- Wait a few minutes
- Upgrade to a paid plan
- Or switch to local LLM (see above)

### Error: "Connection timeout"

**Solution**: Network or API issues
- Check your internet connection
- Verify KRUTRIM_API_URL is correct
- Check Krutrim status: https://status.olakrutrim.com/ (if available)

## 📞 Support

### Krutrim Support
- Website: https://cloud.olakrutrim.com/
- Documentation: https://docs.olakrutrim.com/ (if available)
- Email: support@olakrutrim.com (check their website)

### Astra Support
- GitHub Issues: https://github.com/Harihkvent/skills-copilot-codespaces-vscode/issues
- Documentation: See README.md and other .md files

## 🎯 Best Practices

1. **API Key Security**
   - Never commit your API key to git
   - Use environment variables
   - Rotate keys regularly

2. **Cost Management**
   - Monitor your usage at cloud.olakrutrim.com
   - Set up billing alerts
   - Use caching when possible

3. **Error Handling**
   - Astra has fallback mechanisms
   - Check logs: `docker-compose logs api`
   - Test with simple commands first

4. **Performance**
   - Krutrim API is typically fast (<2s response)
   - If slow, check your network
   - Consider local LLM for offline usage

## 🔐 Security Notes

- **Keep your API key secret**: Never share it publicly
- **Use HTTPS only**: Always ensure secure connections
- **.env file**: Add to .gitignore (already done)
- **Production**: Use secrets management (AWS Secrets Manager, etc.)

## 📚 Additional Resources

- [Krutrim Official Website](https://www.olakrutrim.com/)
- [Astra Documentation](README.md)
- [Docker Setup Guide](DOCKER_SETUP.md)
- [Local Setup Guide](LOCAL_SETUP.md)

---

**Ready to use Krutrim?** Run `./setup.sh` and enter your API key when prompted! 🚀
