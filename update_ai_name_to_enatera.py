#!/usr/bin/env python3
"""
🤖 ENTAERA AI NAME UPDATE SCRIPT
===============================
Updates all AI name references from ENTAERA to ENTAERA
"""

import os
import re
from pathlib import Path

def update_file_content(file_path, replacements):
    """Update file content with AI name replacements"""
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
    """Main AI name update function"""
    print("🤖 ENTAERA AI NAME UPDATE")
    print("=" * 40)
    
    # Define AI name replacements
    replacements = {
        # Main package/framework name changes
        'ENTAERA': 'ENTAERA',
        'entaera': 'entaera',
        'Entaera': 'Entaera',
        
        # URLs and emails  
        'team@entaera.com': 'team@entaera.com',
        'support@entaera.dev': 'support@entaera.dev',
        'developers@entaera.dev': 'developers@entaera.dev',
        'https://entaera.readthedocs.io': 'https://entaera.readthedocs.io',
        'https://docs.entaera.dev': 'https://docs.entaera.dev',
        'ENTAERA-Kata': 'ENTAERA-Kata',
        'entaera-kata': 'entaera-kata',
        
        # Team names
        'ENTAERA Team': 'ENTAERA Team',
        
        # Directory and file references
        '/.entaera/': '/.entaera/',
        '~/.entaera': '~/.entaera',
        'entaera_': 'entaera_',
        'entaera.log': 'entaera.log',
        
        # Import statements (need to be careful with these)
        'from entaera.': 'from entaera.',
        'import entaera.': 'import entaera.',
        'from src.entaera.': 'from src.entaera.',
        'import src.entaera.': 'import src.entaera.',
        
        # Comments and documentation
        '# ENTAERA': '# ENTAERA',
        '## ENTAERA': '## ENTAERA', 
        '### ENTAERA': '### ENTAERA',
        '#### ENTAERA': '#### ENTAERA',
        '##### ENTAERA': '##### ENTAERA',
        
        # Quotes and strings
        '"ENTAERA': '"ENTAERA',
        "'ENTAERA": "'ENTAERA",
        '"entaera': '"entaera',
        "'entaera": "'entaera",
        
        # Docker and deployment
        'entaera:': 'entaera:',
        
        # Command line scripts
        'entaera = "': 'entaera = "',
    }
    
    # File extensions to process
    file_extensions = ['.py', '.md', '.txt', '.toml', '.yml', '.yaml', '.json', '.env', '.example']
    
    # Process all files in current directory and subdirectories
    total_files = 0
    updated_files = 0
    
    current_dir = Path('.')
    
    print(f"\n📁 Processing all files...")
    
    # Find all files with target extensions
    for ext in file_extensions:
        pattern = f"**/*{ext}"
        for file_path in current_dir.glob(pattern):
            if file_path.is_file():
                # Skip certain directories to avoid issues
                if any(skip_dir in str(file_path) for skip_dir in ['.git', '__pycache__', '.pytest_cache', 'node_modules']):
                    continue
                    
                total_files += 1
                if update_file_content(file_path, replacements):
                    updated_files += 1
    
    print(f"\n🎯 AI NAME UPDATE COMPLETE!")
    print(f"📊 Files processed: {total_files}")
    print(f"✅ Files updated: {updated_files}")
    print(f"⚪ Files unchanged: {total_files - updated_files}")
    
    print(f"\n🤖 ENTAERA AI is ready!")
    print(f"🔧 Next step: Rename src/entaera directory to src/entaera")

if __name__ == "__main__":
    main()