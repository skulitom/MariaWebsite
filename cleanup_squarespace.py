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

    # Remove ONLY external Squarespace scripts (keep inline styles!)
    for script in soup.find_all('script'):
        src = script.get('src', '')
        # Only remove external squarespace scripts, NOT inline styles or config
        if src and ('squarespace' in src or 'typekit' in src):
            script.decompose()

    # Remove ONLY external Squarespace stylesheets (keep inline <style> blocks!)
    for link in soup.find_all('link'):
        try:
            href = link.get('href', '')
            if href and ('squarespace' in href or 'typekit' in href):
                link.decompose()
        except:
            continue

    # Keep Squarespace meta tags and config - they don't hurt and may be needed

    # Update image URLs to local paths
    # First, get list of actual image files we have
    images_dir = os.path.join(r'C:\DEV\MARIA\MARIA_WEBSITE\images', section_name)
    available_images = {}
    if os.path.exists(images_dir):
        for img_file in os.listdir(images_dir):
            # Strip section prefix to get original name
            original_name = img_file.replace(f'{section_name}_', '')
            available_images[original_name.lower()] = img_file

    for img in soup.find_all('img'):
        src = img.get('src', '')
        data_src = img.get('data-src', '')

        if 'squarespace-cdn.com' in src:
            # Extract filename from URL (last part before query params)
            filename_match = re.search(r'/([^/\?]+\.(jpg|jpeg|png|gif|webp))', src, re.I)
            if filename_match:
                filename = filename_match.group(1)
                # Find matching local file
                if filename.lower() in available_images:
                    local_file = available_images[filename.lower()]
                    img['src'] = f'./images/{section_name}/{local_file}'
                    # Keep srcset but update it too
                    if img.get('srcset'):
                        del img['srcset']

        if 'squarespace-cdn.com' in data_src:
            filename_match = re.search(r'/([^/\?]+\.(jpg|jpeg|png|gif|webp))', data_src, re.I)
            if filename_match:
                filename = filename_match.group(1)
                if filename.lower() in available_images:
                    local_file = available_images[filename.lower()]
                    img['data-src'] = f'./images/{section_name}/{local_file}'

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

    # Add the downloaded Squarespace CSS files + red background override
    head = soup.find('head')
    if head:
        # Add Squarespace static CSS (base styles)
        link1 = soup.new_tag('link', rel='stylesheet', type='text/css', href='./css/squarespace-static.css')
        head.append(link1)

        # Add Squarespace site CSS (site-specific styles)
        link2 = soup.new_tag('link', rel='stylesheet', type='text/css', href='./css/squarespace-site.css')
        head.append(link2)

        # Add critical CSS fixes at the very end
        style = soup.new_tag('style')
        style.string = '''
        /* Red background override */
        body { background-color: hsla(0, 97%, 55%, 1) !important; }
        .header-announcement-bar-wrapper { background-color: hsla(0, 97%, 55%, 1) !important; }
        #siteWrapper { background-color: hsla(0, 97%, 55%, 1) !important; }

        /* Fix font loading - make text visible immediately with system fonts */
        html.wf-loading * { animation: none !important; color: inherit !important; }
        html { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important; }
        body, p, h1, h2, h3, h4, h5, h6, span, div {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
        }

        /* Ensure scaled text is visible */
        .sqsrte-scaled-text-container, .sqsrte-scaled-text { opacity: 1 !important; visibility: visible !important; }
        '''
        head.append(style)

    # Remove the wf-loading class from html tag to prevent text hiding
    html_tag = soup.find('html')
    if html_tag and html_tag.get('class'):
        classes = html_tag.get('class', [])
        if 'wf-loading' in classes:
            classes.remove('wf-loading')
            if classes:
                html_tag['class'] = classes
            else:
                del html_tag['class']

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
