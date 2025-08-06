#!/usr/bin/env python3
"""
VertexAutoGPT - Autonomous Research Agent

This is the main entry point for the VertexAutoGPT application.
Run this script to start the autonomous research agent.

Usage:
    python main.py                          # Start web interface
    python main.py --cli                   # Use command-line interface
    python main.py --query "research topic"  # Direct research query
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def setup_logging(log_level: str = "INFO"):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('vertexautogpt.log')
        ]
    )

async def start_web_interface():
    """Start the FastAPI web interface."""
    print("🚀 Starting VertexAutoGPT Web Interface...")
    print("📖 Visit http://localhost:8000 for the web interface")
    print("📚 API documentation available at http://localhost:8000/docs")
    
    # Import here to avoid circular imports
    try:
        import uvicorn
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except ImportError:
        print("❌ FastAPI/Uvicorn not installed. Install with: pip install fastapi uvicorn")
    except ModuleNotFoundError:
        print("⚠️  API module not yet implemented. Starting placeholder server...")
        print("🔧 This is a development placeholder. Full implementation coming soon!")

async def start_cli_interface():
    """Start the command-line interface."""
    print("💻 VertexAutoGPT CLI Interface")
    print("🤖 Enter your research queries below (type 'exit' to quit)")
    
    while True:
        try:
            query = input("\n🔍 Research Query: ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                break
            if query:
                await process_query(query)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

async def process_query(query: str):
    """Process a single research query."""
    print(f"🔄 Processing query: {query}")
    print("⚠️  Full agent implementation coming soon!")
    print("🔧 This is a development placeholder.")
    
    # Placeholder for actual agent logic
    print("📊 Results:")
    print(f"   • Query analyzed: {query}")
    print("   • Tools selected: [search, arxiv, summarize]")
    print("   • Status: Ready for implementation")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="VertexAutoGPT - Autonomous Research Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Start web interface
  python main.py --cli                             # Start CLI
  python main.py --query "AI agent architectures"  # Direct query
  python main.py --log-level DEBUG                 # Debug logging
        """
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true', 
        help='Start command-line interface instead of web interface'
    )
    
    parser.add_argument(
        '--query', 
        type=str, 
        help='Process a single research query and exit'
    )
    
    parser.add_argument(
        '--log-level', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
        default='INFO',
        help='Set logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Display banner
    print("=" * 60)
    print("🤖 VertexAutoGPT - Autonomous Research Agent")
    print("   Intelligent research automation with AI")
    print("=" * 60)
    
    try:
        if args.query:
            # Process single query
            logger.info(f"Processing single query: {args.query}")
            asyncio.run(process_query(args.query))
        elif args.cli:
            # Start CLI interface
            logger.info("Starting CLI interface")
            asyncio.run(start_cli_interface())
        else:
            # Start web interface (default)
            logger.info("Starting web interface")
            asyncio.run(start_web_interface())
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()