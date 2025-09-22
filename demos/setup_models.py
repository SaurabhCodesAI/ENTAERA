#!/usr/bin/env python3
"""
ENTAERA-Kata Model Setup Script
====================================

This script helps you download and set up the open-weight models
optimized for RTX 4050 6GB GPU configuration.

Usage:
    python setup_models.py --interactive
    python setup_models.py --auto --gpu-memory 5.5
"""

import os
import sys
import argparse
import requests
import shutil
from pathlib import Path
from typing import List, Dict
import hashlib
from tqdm import tqdm

# Model configurations optimized for RTX 4050
RECOMMENDED_MODELS = {
    "chat": {
        "name": "Llama 3.1 8B Instruct (Q4_K_M)",
        "file": "llama-3.1-8b-instruct.Q4_K_M.gguf", 
        "url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "size_gb": 4.4,
        "description": "General chat and reasoning tasks"
    },
    "code": {
        "name": "CodeLlama 7B Instruct (Q4_K_M)", 
        "file": "codellama-7b-instruct.Q4_K_M.gguf",
        "url": "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf",
        "size_gb": 3.8,
        "description": "Code generation and analysis"
    },
    "embedding": {
        "name": "all-MiniLM-L6-v2",
        "file": "sentence-transformers/all-MiniLM-L6-v2",
        "install_command": "pip install sentence-transformers",
        "size_gb": 0.09,
        "description": "Text embeddings for similarity search"
    }
}

class ModelDownloader:
    """Handles downloading and setting up AI models."""
    
    def __init__(self, models_dir: str = "./models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
    def check_disk_space(self, required_gb: float) -> bool:
        """Check if enough disk space is available."""
        try:
            if os.name == 'nt':  # Windows
                import shutil
                free_space = shutil.disk_usage(self.models_dir).free / (1024**3)
            else:  # Unix/Linux
                statvfs = os.statvfs(self.models_dir)
                free_space = statvfs.f_frsize * statvfs.f_bavail / (1024**3)
            return free_space >= required_gb
        except Exception as e:
            print(f"⚠️ Could not check disk space: {e}")
            return True  # Assume enough space and proceed
    
    def download_file(self, url: str, filepath: Path, chunk_size: int = 8192) -> bool:
        """Download a file with progress bar."""
        try:
            print(f"📥 Downloading {filepath.name}...")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f, tqdm(
                desc=filepath.name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
            
            print(f"✅ Downloaded {filepath.name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download {filepath.name}: {e}")
            return False
    
    def install_embedding_model(self) -> bool:
        """Install sentence-transformers for embeddings."""
        try:
            import subprocess
            print("📦 Installing sentence-transformers...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "sentence-transformers"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ sentence-transformers installed successfully")
                return True
            else:
                print(f"❌ Failed to install sentence-transformers: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error installing sentence-transformers: {e}")
            return False
    
    def setup_models(self, model_types: List[str], gpu_memory_gb: float = 5.5) -> bool:
        """Download and setup selected models."""
        total_size = sum(RECOMMENDED_MODELS[t]["size_gb"] for t in model_types)
        
        print(f"🎯 Setting up models for RTX 4050 ({gpu_memory_gb}GB GPU memory)")
        print(f"📊 Total download size: {total_size:.1f} GB")
        
        # Check disk space
        if not self.check_disk_space(total_size + 1):  # +1GB buffer
            print(f"❌ Insufficient disk space. Need {total_size + 1:.1f} GB free")
            return False
        
        success_count = 0
        
        for model_type in model_types:
            model_info = RECOMMENDED_MODELS[model_type]
            print(f"\n🤖 Setting up {model_info['name']}")
            print(f"   Purpose: {model_info['description']}")
            
            if model_type == "embedding":
                if self.install_embedding_model():
                    success_count += 1
            else:
                filepath = self.models_dir / model_info["file"]
                
                if filepath.exists():
                    print(f"✅ {model_info['name']} already exists")
                    success_count += 1
                else:
                    if self.download_file(model_info["url"], filepath):
                        success_count += 1
        
        print(f"\n📈 Setup Results: {success_count}/{len(model_types)} models ready")
        return success_count == len(model_types)
    
    def create_config_file(self, gpu_memory_gb: float = 5.5):
        """Create optimized configuration file."""
        config_content = f"""# ENTAERA-Kata Local AI Configuration
# Auto-generated for RTX 4050 {gpu_memory_gb}GB setup

# Local Model Configuration
LOCAL_AI_ENABLED=true
CUDA_ENABLED=true
MAX_GPU_MEMORY_GB={gpu_memory_gb}
DEVICE=cuda

# Model Paths
CODE_MODEL_PATH=./models/codellama-7b-instruct.Q4_K_M.gguf
CHAT_MODEL_PATH=./models/llama-3.1-8b-instruct.Q4_K_M.gguf
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Optimized Settings
MODEL_CONTEXT_LENGTH=4096
MAX_TOKENS_PER_REQUEST=512
TEMPERATURE=0.1
USE_QUANTIZATION=true
QUANTIZATION_TYPE=Q4_K_M
NUM_GPU_LAYERS=35

# Fallback to APIs when needed
LOCAL_FIRST=true
API_FALLBACK_ENABLED=true
MAX_LOCAL_COMPLEXITY_SCORE=0.7
LOCAL_TIMEOUT_SECONDS=30
"""
        
        config_path = Path(".env.local_ai")
        config_path.write_text(config_content)
        print(f"✅ Created configuration file: {config_path}")


def interactive_setup():
    """Interactive setup process."""
    print("🎯 ENTAERA-Kata Model Setup")
    print("=" * 50)
    
    # GPU memory detection
    try:
        import torch
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"🔍 Detected GPU: {torch.cuda.get_device_name(0)}")
            print(f"💾 GPU Memory: {gpu_memory:.1f} GB")
        else:
            print("⚠️  No CUDA GPU detected. Local models will run on CPU (slower)")
            gpu_memory = 0
    except ImportError:
        print("⚠️  PyTorch not installed. Cannot detect GPU")
        gpu_memory = float(input("Enter your GPU memory in GB (or 0 for CPU): "))
    
    # Model selection
    print("\n🤖 Available Models:")
    for i, (key, model) in enumerate(RECOMMENDED_MODELS.items(), 1):
        print(f"  {i}. {model['name']} ({model['size_gb']:.1f} GB)")
        print(f"     {model['description']}")
    
    print("\nRecommended setup for RTX 4050:")
    print("  • Chat model (4.4 GB) - Essential")
    print("  • Code model (3.8 GB) - For programming tasks") 
    print("  • Embedding model (0.1 GB) - For search/similarity")
    
    choice = input("\nDownload all recommended models? (y/n): ").lower().strip()
    
    if choice == 'y':
        selected_models = ["chat", "code", "embedding"]
    else:
        selected_models = []
        for key, model in RECOMMENDED_MODELS.items():
            choice = input(f"Download {model['name']}? (y/n): ").lower().strip()
            if choice == 'y':
                selected_models.append(key)
    
    if not selected_models:
        print("❌ No models selected. Exiting.")
        return
    
    # Download models
    downloader = ModelDownloader()
    if downloader.setup_models(selected_models, max(gpu_memory - 0.5, 4.0)):
        downloader.create_config_file(max(gpu_memory - 0.5, 4.0))
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Copy .env.local_ai to .env.development")
        print("2. Add your API keys for fallback providers")
        print("3. Run: python examples/basic_usage/hello_world.py")
    else:
        print("\n❌ Setup failed. Check error messages above.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Setup ENTAERA-Kata models")
    parser.add_argument("--interactive", action="store_true", help="Interactive setup")
    parser.add_argument("--auto", action="store_true", help="Automatic setup")
    parser.add_argument("--gpu-memory", type=float, default=5.5, help="GPU memory in GB")
    parser.add_argument("--models", nargs="+", choices=["chat", "code", "embedding"], 
                       default=["chat", "code", "embedding"], help="Models to download")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_setup()
    elif args.auto:
        downloader = ModelDownloader()
        if downloader.setup_models(args.models, args.gpu_memory):
            downloader.create_config_file(args.gpu_memory)
            print("🎉 Automatic setup completed!")
        else:
            print("❌ Automatic setup failed.")
    else:
        print("Use --interactive for guided setup or --auto for automatic setup")
        print("Example: python setup_models.py --interactive")


if __name__ == "__main__":
    main()