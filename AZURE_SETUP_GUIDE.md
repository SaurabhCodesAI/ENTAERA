🔵 AZURE OPENAI SETUP GUIDE FOR ENTAERA
========================================

📋 CURRENT STATUS:
✅ Gemini API: Working
✅ Perplexity API: Configured (model name issue to fix)
❌ Azure OpenAI: Needs setup

🎯 TO GET AZURE OPENAI WORKING:

1️⃣ Go to Azure Portal:
   https://portal.azure.com/

2️⃣ Create Azure OpenAI Resource:
   - Search "Azure OpenAI" 
   - Click "Create"
   - Choose subscription & resource group
   - Pick a region (like East US)
   - Give it a name (like "entaera-openai")
   - Click "Create"

3️⃣ Deploy a Model:
   - Go to your Azure OpenAI resource
   - Click "Model deployments" → "Go to Azure OpenAI Studio"
   - Click "Deployments" → "Create new deployment"
   - Choose model: "gpt-35-turbo" 
   - Give deployment name: "gpt-35-turbo"
   - Click "Create"

4️⃣ Get Your Credentials:
   - In Azure portal, go to your OpenAI resource
   - Click "Keys and Endpoint"
   - Copy:
     * KEY 1 (your API key)
     * Endpoint URL (like https://your-name.openai.azure.com/)

5️⃣ Update Your .env File:
   Replace these lines in your .env:
   
   AZURE_OPENAI_API_KEY=your_actual_azure_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   
   (Keep the rest as is)

6️⃣ Test It:
   python azure_continuous_test.py

💰 COST: 
- Azure gives $200 free credit for new accounts
- GPT-3.5-turbo costs ~$0.002 per 1K tokens (very cheap!)

⏱️ TIME NEEDED: 
- 5-10 minutes to set up
- Then you'll have enterprise-grade AI!

🚀 WHY AZURE OPENAI?
- Most reliable API
- Enterprise security
- Better rate limits
- ENTAERA will use it for production workloads

📞 ALTERNATIVE (if you want to test NOW):
You can also get OpenAI direct API key from:
https://platform.openai.com/api-keys

Then add to .env:
OPENAI_API_KEY=your_openai_key_here

This will work immediately with ENTAERA!