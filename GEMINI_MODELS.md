# Gemini Models - Complete List

## ✅ Currently Using: `gemini-2.5-flash`

Latest stable Gemini model (July 2025 release)

---

## 📋 All Available Models (50 Total)

### 🌟 RECOMMENDED - Latest Stable

| Model | Description | Best For |
|-------|-------------|----------|
| `gemini-2.5-flash` | **Latest stable** (July 2025) | General use, fast & accurate |
| `gemini-2.5-pro` | Most capable | Complex tasks, deep analysis |
| `gemini-flash-latest` | Auto-updates to newest | Always latest version |
| `gemini-pro-latest` | Auto-updates to newest Pro | Most powerful available |

### ⚡ FASTEST - For Speed

| Model | Description |
|-------|-------------|
| `gemini-2.5-flash-lite` | Ultra-fast lightweight |
| `gemini-2.0-flash-lite` | Fast lightweight |

### 🏗️ STABLE - Production Ready

| Model | Version | Release |
|-------|---------|---------|
| `gemini-2.5-pro` | Latest Pro | June 17, 2025 |
| `gemini-2.5-flash` | Latest Flash | July 2025 |
| `gemini-2.0-flash` | Flash 2.0 | 2024 |
| `gemini-2.0-flash-001` | Flash 2.0 versioned | 2024 |

### 🧪 EXPERIMENTAL - Preview/Testing

| Model | Type |
|-------|------|
| `gemini-2.5-pro-preview-06-05` | Pro Preview |
| `gemini-2.5-flash-preview-09-2025` | Flash Preview |
| `gemini-2.0-flash-exp` | Flash Experimental |
| `gemini-2.0-pro-exp` | Pro Experimental |
| `gemini-exp-1206` | Experimental 1206 |

### 🎨 SPECIALIZED - Special Features

| Model | Feature |
|-------|---------|
| `gemini-2.0-flash-exp-image-generation` | Image generation |
| `gemini-2.5-flash-image` | Image generation |
| `gemini-2.5-flash-preview-tts` | Text-to-speech |
| `gemini-2.5-pro-preview-tts` | Text-to-speech Pro |
| `gemini-2.5-computer-use-preview-10-2025` | Computer control |

### 🤖 GEMMA - Smaller Models

| Model | Size |
|-------|------|
| `gemma-3-27b-it` | 27B parameters |
| `gemma-3-12b-it` | 12B parameters |
| `gemma-3-4b-it` | 4B parameters |
| `gemma-3-1b-it` | 1B parameters |

### 📚 OTHER SPECIALIZED

- `learnlm-2.0-flash-experimental` - Learning-focused
- `gemini-robotics-er-1.5-preview` - Robotics
- Thinking models: `gemini-2.0-flash-thinking-exp`

---

## 🎯 Our Configuration

**File:** `agent.py`

```python
# Using latest stable Gemini 2.5 Flash
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
```

### Why Gemini 2.5 Flash?

✅ **Latest stable** - Released July 2025  
✅ **Faster** - Improved performance over 2.0  
✅ **Better quality** - Enhanced responses  
✅ **Production ready** - Not experimental  
✅ **Free tier** - Works with existing API keys  

### Alternative Options

**For maximum power:** Use `gemini-2.5-pro`
```python
url = f"...models/gemini-2.5-pro:generateContent?key={api_key}"
```

**For maximum speed:** Use `gemini-2.5-flash-lite`
```python
url = f"...models/gemini-2.5-flash-lite:generateContent?key={api_key}"
```

**For auto-updates:** Use `gemini-flash-latest`
```python
url = f"...models/gemini-flash-latest:generateContent?key={api_key}"
```

---

## 📊 Models NOT for Text Generation

These are embedding/image models (40 total models support generateContent):

- `embedding-001` - Text embeddings
- `text-embedding-004` - Text embeddings  
- `imagen-3.0-generate-002` - Image generation
- `imagen-4.0-generate-preview-06-06` - Image preview
- `aqa` - Question answering

---

## 🔑 API Key Management

All models use the same API keys:
- `GEMINI_API_KEY` 
- `GEMINI_API_KEY_2`
- `GEMINI_API_KEY_3`

Get keys at: https://aistudio.google.com/apikey

---

## ✅ Status

**Current Setup:**
- ✅ Gemini 2.5 Flash - Working
- ✅ 3 API keys configured (rotation enabled)
- ✅ Automatic fallback to Ollama
- ✅ Rate limit handling

**Test Command:**
```bash
python agent.py
# Ask: "Write a haiku about AI"
```

---

*Last updated: November 2, 2025*  
*Total models available: 50*  
*Models supporting generateContent: 40*
