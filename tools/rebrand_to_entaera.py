#!/usr/bin/env python3
"""
🔄 COMPREHENSIVE ENTAERA REBRANDING SCRIPT
==========================================
Renames all ENTAERA references to ENTAERA throughout the codebase
"""

import os
import re
import sys
from pathlib import Path

def update_file_content(file_path, replacements):
    """Update file content with multiple replacements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        # If content changed, write it back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⚪ No changes: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main rebranding function"""
    print("🔄 COMPREHENSIVE ENTAERA REBRANDING")
    print("=" * 50)
    
    # Define all replacements
    replacements = {
        # Package names
        'entaera': 'entaera',
        'ENTAERA': 'ENTAERA',
        'entaera': 'entaera',
        
        # Import statements
        'from entaera.': 'from entaera.',
        'import entaera.': 'import entaera.',
        'from src.entaera.': 'from src.entaera.',
        'import src.entaera.': 'import src.entaera.',
        
        # URLs and emails
        'team@entaera.com': 'team@entaera.com',
        'support@entaera.dev': 'support@entaera.dev',
        'developers@entaera.dev': 'developers@entaera.dev',
        'https://entaera.readthedocs.io': 'https://entaera.readthedocs.io',
        'https://docs.entaera.dev': 'https://docs.entaera.dev',
        'https://github.com/yourusername/ENTAERA-Kata': 'https://github.com/yourusername/ENTAERA-Kata',
        'ENTAERA-Kata': 'ENTAERA-Kata',
        'entaera-kata': 'entaera-kata',
        
        # Organization/Team names
        'ENTAERA Team': 'ENTAERA Team',
        
        # Directory references
        '/.entaera/': '/.entaera/',
        '~/.entaera': '~/.entaera',
        'entaera_': 'entaera_',
        
        # File patterns
        'entaera.log': 'entaera.log',
        '"ENTAERA': '"ENTAERA',
        "'ENTAERA": "'ENTAERA",
        
        # Command line tools
        'entaera = "': 'entaera = "',
        
        # Docker and deployment
        'entaera:': 'entaera:',
        'entaera_': 'entaera_',
        
        # Comments and documentation
        '# ENTAERA': '# ENTAERA',
        '## ENTAERA': '## ENTAERA',
        '### ENTAERA': '### ENTAERA',
        '#### ENTAERA': '#### ENTAERA',
        '##### ENTAERA': '##### ENTAERA',
    }
    
    # File extensions to process
    file_extensions = ['.py', '.md', '.txt', '.toml', '.yml', '.yaml', '.json', '.env', '.example']
    
    # Directories to process (from current directory)
    directories_to_process = [
        'src',
        'tests', 
        'docs',
        'examples',
        '.'  # Root directory files
    ]
    
    total_files = 0
    updated_files = 0
    
    # Process each directory
    for directory in directories_to_process:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"⚠️ Directory not found: {directory}")
            continue
            
        print(f"\n📁 Processing directory: {directory}")
        
        # Find all files with target extensions
        for ext in file_extensions:
            pattern = f"**/*{ext}"
            for file_path in dir_path.glob(pattern):
                if file_path.is_file():
                    total_files += 1
                    if update_file_content(file_path, replacements):
                        updated_files += 1
    
    # Process specific root files
    root_files = [
        'README.md',
        'pyproject.toml', 
        '.env.example',
        '.env.development',
        '.env.production.example',
        'Dockerfile',
        'docker-compose.yml',
        'docker-compose.prod.yml',
        'setup.py',
        'requirements.txt',
        'requirements-local-ai.txt',
        'requirements-optimal.txt'
    ]
    
    print(f"\n📄 Processing root files...")
    for filename in root_files:
        file_path = Path(filename)
        if file_path.exists():
            total_files += 1
            if update_file_content(file_path, replacements):
                updated_files += 1
    
    print(f"\n🎯 REBRANDING COMPLETE!")
    print(f"📊 Files processed: {total_files}")
    print(f"✅ Files updated: {updated_files}")
    print(f"⚪ Files unchanged: {total_files - updated_files}")
    
    print(f"\n🚀 ENTAERA is ready!")
    print(f"🔧 Next: Test imports with 'python -c \"import entaera; print(\\'Success!\\')\"'")

if __name__ == "__main__":
    main()