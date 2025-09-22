"""
Text Processing Utilities for ENTAERA

This module provides text normalization and processing functions with support for:
- Unicode handling and emoji processing
- Whitespace normalization
- Regex-based text cleaning
- Performance-optimized implementations

Kata Learning Objectives:
- String manipulation in Python
- Regular expressions basics
- Unicode handling
- Function documentation
- Type hints and error handling
"""

import re
import unicodedata
from typing import Optional


def normalize_text(text: str) -> str:
    """
    Normalize text by:
    - Converting to lowercase
    - Removing extra whitespace
    - Handling emojis consistently
    - Preserving meaningful punctuation
    
    This function is designed as Kata 1.2: Text Normalization
    
    Args:
        text (str): Input text to normalize
        
    Returns:
        str: Normalized text
        
    Examples:
        >>> normalize_text("  Hello   WORLD! 👋  ")
        'hello world! 👋'
        
        >>> normalize_text("Multiple    spaces   everywhere")
        'multiple spaces everywhere'
        
        >>> normalize_text("")
        ''
        
    Raises:
        TypeError: If input is not a string
        
    Performance:
        - Optimized for large texts
        - Memory efficient with regex compilation
        - Handles Unicode properly
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    
    # Handle empty or whitespace-only strings
    if not text or text.isspace():
        return ""
    
    # Step 1: Convert to lowercase
    normalized = text.lower()
    
    # Step 2: Normalize Unicode characters (NFC normalization)
    # This ensures consistent representation of accented characters
    normalized = unicodedata.normalize('NFC', normalized)
    
    # Step 3: Remove extra whitespace but preserve single spaces
    # This regex replaces multiple whitespace characters with single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Step 4: Strip leading and trailing whitespace
    normalized = normalized.strip()
    
    return normalized


def contains_emoji(text: str) -> bool:
    """
    Check if text contains emoji characters.
    
    This function detects various types of emojis including:
    - Standard emoji characters
    - Emoji with skin tone modifiers
    - Compound emojis with zero-width joiners
    
    Args:
        text (str): Text to check for emojis
        
    Returns:
        bool: True if text contains emojis, False otherwise
        
    Examples:
        >>> contains_emoji("Hello 👋")
        True
        
        >>> contains_emoji("Hello world")
        False
        
        >>> contains_emoji("👨‍💻 Developer")
        True
    """
    if not isinstance(text, str):
        return False
    
    # Unicode ranges for emoji characters
    # This pattern covers most emoji ranges in Unicode including ZWJ sequences
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        "\U0000200D"             # zero-width joiner
        "]+", 
        flags=re.UNICODE
    )
    
    return bool(emoji_pattern.search(text))


def remove_emojis(text: str) -> str:
    """
    Remove all emoji characters from text.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Text with emojis removed
        
    Examples:
        >>> remove_emojis("Hello 👋 world 🌍!")
        'Hello  world !'
        
        >>> remove_emojis("No emojis here")
        'No emojis here'
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    
    # Use the same emoji pattern as contains_emoji (including ZWJ)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        "\U0000200D"             # zero-width joiner
        "]+", 
        flags=re.UNICODE
    )
    
    # Remove emojis and clean up extra spaces
    result = emoji_pattern.sub('', text)
    return re.sub(r'\s+', ' ', result).strip()


def extract_emojis(text: str) -> list[str]:
    """
    Extract all emoji characters from text.
    
    Args:
        text (str): Input text
        
    Returns:
        list[str]: List of emoji characters found
        
    Examples:
        >>> extract_emojis("Hello 👋 world 🌍!")
        ['👋', '🌍']
        
        >>> extract_emojis("No emojis here")
        []
    """
    if not isinstance(text, str):
        return []
    
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        "\U0000200D"             # zero-width joiner
        "]", 
        flags=re.UNICODE
    )
    
    return emoji_pattern.findall(text)


def normalize_text_advanced(
    text: str,
    remove_emojis_flag: bool = False,
    preserve_case: bool = False,
    remove_punctuation: bool = False
) -> str:
    """
    Advanced text normalization with configurable options.
    
    This is an extended version of normalize_text with additional options
    for more specific use cases.
    
    Args:
        text (str): Input text to normalize
        remove_emojis_flag (bool): Whether to remove emoji characters
        preserve_case (bool): Whether to preserve original case
        remove_punctuation (bool): Whether to remove punctuation
        
    Returns:
        str: Normalized text according to specified options
        
    Examples:
        >>> normalize_text_advanced("Hello 👋 WORLD!!!", remove_emojis_flag=True)
        'hello world!!!'
        
        >>> normalize_text_advanced("Hello WORLD", preserve_case=True)
        'Hello WORLD'
        
        >>> normalize_text_advanced("Hello, world!", remove_punctuation=True)
        'hello world'
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    
    if not text or text.isspace():
        return ""
    
    result = text
    
    # Remove emojis if requested
    if remove_emojis_flag:
        result = remove_emojis(result)
    
    # Handle case conversion
    if not preserve_case:
        result = result.lower()
    
    # Normalize Unicode
    result = unicodedata.normalize('NFC', result)
    
    # Remove punctuation if requested
    if remove_punctuation:
        # Keep only alphanumeric characters, whitespace, and emojis
        if remove_emojis_flag:
            result = re.sub(r'[^\w\s]', '', result, flags=re.UNICODE)
        else:
            # More complex pattern to preserve emojis while removing punctuation
            result = re.sub(r'[^\w\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]', '', result, flags=re.UNICODE)
    
    # Normalize whitespace
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result


# Pre-compiled regex patterns for performance
_WHITESPACE_PATTERN = re.compile(r'\s+')
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosed characters
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
    "\U0000200D"             # zero-width joiner
    "]+", 
    flags=re.UNICODE
)


def normalize_text_fast(text: str) -> str:
    """
    High-performance version of normalize_text using pre-compiled patterns.
    
    This version is optimized for processing large volumes of text by using
    pre-compiled regex patterns.
    
    Args:
        text (str): Input text to normalize
        
    Returns:
        str: Normalized text
        
    Performance:
        - Uses pre-compiled regex patterns
        - Minimal function call overhead
        - Optimized for batch processing
    """
    if not isinstance(text, str) or not text or text.isspace():
        return ""
    
    # Use pre-compiled patterns for better performance
    normalized = text.lower()
    normalized = unicodedata.normalize('NFC', normalized)
    normalized = _WHITESPACE_PATTERN.sub(' ', normalized).strip()
    
    return normalized


# Export public functions
__all__ = [
    'normalize_text',
    'contains_emoji', 
    'remove_emojis',
    'extract_emojis',
    'normalize_text_advanced',
    'normalize_text_fast'
]