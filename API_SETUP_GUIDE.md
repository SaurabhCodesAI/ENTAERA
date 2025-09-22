🔑 ENTAERA API SETUP GUIDE
==========================

Your .env file is ready! Here's how to get your API keys:

🚀 QUICK START PRIORITY (recommended order):

1️⃣ AZURE OPENAI (Most reliable, best for production)
   📍 URL: https://portal.azure.com/
   
   Steps:
   a) Create Azure account (free $200 credit!)
   b) Create "Azure OpenAI" resource
   c) Deploy "gpt-35-turbo" model
   d) Get your:
      - API Key from "Keys and Endpoint"
      - Endpoint URL (looks like: https://your-name.openai.azure.com/)
      - Deployment name (usually "gpt-35-turbo")
   
   Update in .env:
   AZURE_OPENAI_API_KEY=your_actual_azure_key
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_DEPLOYMENT_NAME=your_deployment_name

2️⃣ GOOGLE GEMINI (Free tier available)
   📍 URL: https://makersuite.google.com/app/apikey
   
   Steps:
   a) Sign in with Google account
   b) Create new API key
   c) Copy the key
   
   Update in .env:
   GEMINI_API_KEY=your_actual_gemini_key

3️⃣ PERPLEXITY AI (Great for research)
   📍 URL: https://www.perplexity.ai/settings/api
   
   Steps:
   a) Create Perplexity account
   b) Go to API settings
   c) Generate API key
   
   Update in .env:
   PERPLEXITY_API_KEY=your_actual_perplexity_key

4️⃣ OPENAI DIRECT (Optional backup)
   📍 URL: https://platform.openai.com/api-keys
   
   Update in .env:
   OPENAI_API_KEY=your_actual_openai_key

💡 TESTING PRIORITY:
Start with just ONE API key to test, then add others:

Priority 1: Azure OpenAI (most reliable)
Priority 2: Gemini (free and powerful)
Priority 3: Perplexity (for research tasks)

🧪 AFTER ADDING KEYS:
Run: python entaera_api_chat_demo.py

You'll see LIVE API responses instead of demo messages!

🔐 SECURITY NOTES:
- Never commit .env file to Git
- Keep API keys private
- Monitor usage/costs
- Use rate limiting (already configured)

💰 COST ESTIMATES:
- Azure: ~$0.002 per 1k tokens
- Gemini: FREE tier (15 requests/minute)
- Perplexity: FREE tier (5 requests/day)
- OpenAI: ~$0.002 per 1k tokens

🎯 WHICH TO START WITH?
If you want immediate results: Start with Gemini (free + easy)
If you want production-ready: Start with Azure (reliable + scalable)