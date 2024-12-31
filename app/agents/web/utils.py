"""
Utility functions for web-related tasks.
"""

def clean_text(text: str) -> str:
    """
    Clean up extracted text content.
    
    Args:
        text: Raw text content
    
    Returns:
        Cleaned text content
    """
    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return ' '.join(chunk for chunk in chunks if chunk) 