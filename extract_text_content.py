#!/usr/bin/env python3
"""
Extract text content from original Squarespace HTML files
"""

from bs4 import BeautifulSoup
import os
import json

def extract_text_from_html(html_file):
    """Extract meaningful text content from HTML"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    text_content = []

    # Find all text blocks
    for block in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        text = block.get_text(strip=True)
        if text and len(text) > 1:  # Ignore empty or single-char text
            # Get tag name
            tag = block.name
            # Clean up text
            text = text.replace('\xa0', ' ').strip()
            if text not in ['CONTACT', 'FOLLOW', 'WEBSITES']:  # Skip footer duplicates
                text_content.append({
                    'tag': tag,
                    'text': text
                })

    return text_content

def main():
    base_path = r'C:\DEV\MARIA\MARIA_DATA'
    sections = ['home', 'projects', 'photoshoots', 'press', 'press-loans']

    all_content = {}

    for section in sections:
        html_file = os.path.join(base_path, section, 'index.html')
        if os.path.exists(html_file):
            print(f"\n=== {section.upper()} ===")
            content = extract_text_from_html(html_file)
            all_content[section] = content

            for item in content[:20]:  # Show first 20 items
                try:
                    print(f"{item['tag']}: {item['text']}")
                except UnicodeEncodeError:
                    print(f"{item['tag']}: [text with special characters]")

    # Save to JSON
    output_file = r'C:\DEV\MARIA\MARIA_WEBSITE\text_content.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_content, f, indent=2, ensure_ascii=False)

    print(f"\n\nSaved all content to {output_file}")

if __name__ == '__main__':
    main()
