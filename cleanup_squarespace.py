#!/usr/bin/env python3
"""
Clean up Squarespace HTML files with minimal changes
- Remove Squarespace scripts
- Update image URLs to local paths
- Keep all content and structure
"""

from bs4 import BeautifulSoup
import re
import os

def cleanup_html(input_file, output_file, section_name):
    """Clean up Squarespace HTML with minimal changes"""

    print(f"\nProcessing {section_name}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Remove Squarespace scripts
    for script in soup.find_all('script'):
        # Keep only our custom navigation script
        src = script.get('src', '')
        if 'squarespace' in src or 'typekit' in src:
            script.decompose()
        elif script.string and ('SQUARESPACE' in script.string or 'Static.' in script.string):
            script.decompose()

    # Remove Squarespace stylesheets
    for link in soup.find_all('link'):
        try:
            if link and link.get('rel') and 'stylesheet' in str(link.get('rel')):
                href = link.get('href', '')
                if 'squarespace' in href or 'typekit' in href:
                    link.decompose()
        except:
            continue

    # Remove Squarespace meta tags
    for meta in soup.find_all('meta'):
        content = str(meta)
        if 'squarespace' in content.lower():
            meta.decompose()

    # Update image URLs to local paths
    for img in soup.find_all('img'):
        src = img.get('src', '')
        data_src = img.get('data-src', '')

        if 'squarespace-cdn.com' in src:
            # Extract filename from URL
            filename_match = re.search(r'/([^/]+\.(jpg|jpeg|png|gif|webp))', src, re.I)
            if filename_match:
                filename = filename_match.group(1)
                # Update to local path
                img['src'] = f'./images/{section_name}/{section_name}_{filename}'
                # Remove srcset to simplify
                if img.get('srcset'):
                    del img['srcset']

        if 'squarespace-cdn.com' in data_src:
            filename_match = re.search(r'/([^/]+\.(jpg|jpeg|png|gif|webp))', data_src, re.I)
            if filename_match:
                filename = filename_match.group(1)
                img['data-src'] = f'./images/{section_name}/{section_name}_{filename}'

    # Update navigation links
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href == '/':
            a['href'] = 'index.html'
        elif href == '/projects':
            a['href'] = 'projects.html'
        elif href == '/photoshoots':
            a['href'] = 'photoshoots.html'
        elif href == '/press':
            a['href'] = 'press.html'
        elif href == '/press-loans':
            a['href'] = 'press-loans.html'
        elif href == '/about':
            # Remove About Me link (404)
            a.parent.decompose() if a.parent else a.decompose()

    # Add our CSS files to head
    head = soup.find('head')
    if head:
        # Add our custom CSS
        css_files = ['main.css', 'header.css', 'footer.css', 'responsive.css']
        for css_file in css_files:
            link = soup.new_tag('link', rel='stylesheet', href=f'./css/{css_file}')
            head.append(link)

        # Add our navigation script
        script = soup.new_tag('script', src='./js/navigation.js')
        head.append(script)

    # Write cleaned HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    print(f"  Cleaned HTML written to {output_file}")

def main():
    """Process all pages"""

    base_input = r'C:\DEV\MARIA\MARIA_DATA'
    base_output = r'C:\DEV\MARIA\MARIA_WEBSITE'

    pages = [
        ('home', 'index.html'),
        ('projects', 'projects.html'),
        ('photoshoots', 'photoshoots.html'),
        ('press', 'press.html'),
        ('press-loans', 'press-loans.html'),
    ]

    for section, output_filename in pages:
        input_file = os.path.join(base_input, section, 'index.html')
        output_file = os.path.join(base_output, output_filename)

        cleanup_html(input_file, output_file, section)

    print("\nAll pages cleaned successfully!")
    print("\nNote: You may need to manually adjust image paths if filenames don't match exactly.")

if __name__ == '__main__':
    main()
