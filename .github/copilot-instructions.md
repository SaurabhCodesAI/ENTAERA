# ENTAERA-Kata: AI Agent Guidance

## Project Architecture & Components

This project implements a kata-driven AI research agent using a modular architecture:

- **Core Module** (`src/entaera/core/`): Central components including configuration management (`config.py`) and logging infrastructure (`logger.py`).
- **Utils Module** (`src/entaera/utils/`): Helper functions including text processing (`text_processor.py`) and file operations (`files.py`).
- **Providers** (planned): Implementations for different AI providers (Gemini, Perplexity, etc.) using a common interface pattern.

## Key Design Patterns

1. **Configuration Management**: Uses Pydantic for type-safe configuration with validation.
   ```python
   # From src/entaera/core/config.py
   class APIProviderSettings(BaseModel):
       gemini_api_key: str = Field(..., description="Google Gemini API key")
       perplexity_api_key: str = Field(..., description="Perplexity API key")
       
       @field_validator('gemini_api_key', 'perplexity_api_key')
       def validate_api_keys(cls, v):
           if not v or v == "your_api_key_here" or len(v) < 10:
               raise ValueError("API key must be provided and valid")
   ```

2. **Logging Infrastructure**: Implements structured JSON logging with context tracking.
   ```python
   # From src/entaera/core/logger.py
   # Usage pattern:
   logger = get_logger(__name__)
   logger.info("Operation completed", extra={"operation_id": "123"})
   ```

## Development Workflow

### Setup Process
1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
4. Install in dev mode: `pip install -e .`
5. Copy and configure environment: `cp .env.example .env`

### Testing Approach
- Unit tests for components follow a kata-based learning progression
- Tests are organized in `/tests/unit/` directory with day-specific modules
- Run tests: `python -m pytest tests/unit`

### Code Structure Conventions

- Follow the kata progression model: Each component implements learning objectives for a specific day
- Docstrings include kata level, learning objectives, and implementation notes
- Prioritize clean, well-documented code over complex optimizations

## Integration Points

1. **AI Provider Integration**
   - Provider implementations should follow the abstract base class pattern
   - API keys are managed through environment variables and config

2. **Text Processing Pipeline**
   - Input text flows through preprocessing → semantic analysis → response generation
   - Each stage has defined interfaces for extending functionality

## Project Roadmap
- The project follows a 30-day kata progression across 7 levels
- Currently focused on Level 1: Foundation Kata (Days 1-3)
- Each level builds on previous skills following deliberate practice principles

## Troubleshooting
- Log files are stored in `./logs` by default
- Set `LOG_LEVEL=DEBUG` in `.env` for verbose logging
- Most common issues relate to API key configuration