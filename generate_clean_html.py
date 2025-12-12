#!/usr/bin/env python3
"""
Generate clean, semantic HTML for Maria Goundry Portfolio
Replaces complex Squarespace structure with simple HTML + CSS Grid
"""

from bs4 import BeautifulSoup
import json
import os
import re

# Paths
BASE_INPUT = r'C:\DEV\MARIA\MARIA_DATA'
BASE_OUTPUT = r'C:\DEV\MARIA\MARIA_WEBSITE'
TEXT_CONTENT_FILE = os.path.join(BASE_OUTPUT, 'text_content.json')

def extract_images_from_html(html_file, section_name):
    """Extract all image paths from original HTML in order"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    images = []

    # Find all img tags
    for img in soup.find_all('img'):
        src = img.get('src', '') or img.get('data-src', '')
        if src:
            # Extract filename
            filename_match = re.search(r'/([^/\?]+\.(jpg|jpeg|png|gif|webp))', src, re.I)
            if filename_match:
                filename = filename_match.group(1)
                # Convert to local path
                local_path = f'./images/{section_name}/{filename}'
                # Check if file exists (some filenames have section prefix)
                images.append(local_path)

    return images

def generate_nav():
    """Generate navigation HTML"""
    return '''    <nav class="main-nav">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="projects.html">Projects</a></li>
        <li><a href="photoshoots.html">Photoshoots</a></li>
        <li><a href="press.html">Press</a></li>
        <li><a href="press-loans.html">Press Loans</a></li>
      </ul>
    </nav>'''

def generate_footer():
    """Generate footer HTML"""
    return '''    <footer class="main-footer">
      <p>EMAIL: maria.goundry98@gmail.com</p>
      <a href="https://instagram.com/mariagoundry" target="_blank">INSTAGRAM</a>
      <a href="https://www.notjustalabel.com/designer/maria-goundry" target="_blank">NOT JUST A LABEL</a>
      <a href="https://neighbourhoodmagazine.com/contributors/maria-goundry/" target="_blank">NEIGHBOURHOOD MAGAZINE</a>
    </footer>'''

def generate_home_html(text_data, images):
    """Generate home page HTML"""
    print("\n=== Generating HOME page ===")

    # Filter out footer items
    content_items = [item for item in text_data if not item['text'].startswith(('EMAIL', 'INSTAGRAM', 'NOT JUST', 'NEIGHBOURHOOD'))]

    # Extract hero content
    hero_title1 = content_items[0]['text'] if len(content_items) > 0 else "MARIA GOUNDRY"
    hero_title2 = content_items[1]['text'] if len(content_items) > 1 else "PORTFOLIO"
    hero_intro = content_items[2]['text'] if len(content_items) > 2 else ""

    # Build sections
    sections_html = ""
    current_section = {}

    for i, item in enumerate(content_items[3:], start=3):  # Skip hero items
        if item['tag'] in ['h2', 'h3']:
            # Save previous section
            if current_section:
                sections_html += generate_home_section(current_section, images)
            # Start new section
            current_section = {
                'title': item['text'],
                'description': '',
                'images': []
            }
        elif item['tag'] == 'p' and current_section:
            # Add to description
            if not item['text'].startswith('→'):
                current_section['description'] += item['text'] + ' '

    # Add last section
    if current_section:
        sections_html += generate_home_section(current_section, images)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Maria Goundry Portfolio</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
{generate_nav()}

    <header class="hero">
      <h1 class="hero-title">{hero_title1}</h1>
      <h1 class="hero-title">{hero_title2}</h1>
      <p class="hero-intro">{hero_intro}</p>
    </header>

{sections_html}

{generate_footer()}
  </div>
</body>
</html>'''

    return html

def generate_home_section(section, all_images):
    """Generate a home section with images"""
    # Take first 6 images for preview
    images_html = ""
    if all_images:
        img_count = min(6, len(all_images))
        for i in range(img_count):
            if i < len(all_images):
                images_html += f'''        <img src="{all_images[i]}" alt="{section['title']}">\n'''

    return f'''    <section class="home-section">
      <h2>{section['title']}</h2>
      <p>{section['description'].strip()}</p>
      <div class="section-preview">
{images_html}      </div>
    </section>

'''

def generate_projects_html(text_data, images):
    """Generate projects page HTML"""
    print("\n=== Generating PROJECTS page ===")

    # Filter out footer items
    content_items = [item for item in text_data if not item['text'].startswith(('EMAIL', 'INSTAGRAM', 'NOT JUST', 'NEIGHBOURHOOD'))]

    # Group projects (h2 + h3 pairs)
    projects = []
    current_project = None

    for item in content_items:
        if item['tag'] == 'h2':
            if current_project:
                projects.append(current_project)
            current_project = {
                'title': item['text'],
                'year': ''
            }
        elif item['tag'] == 'h3' and current_project:
            current_project['year'] = item['text']

    if current_project:
        projects.append(current_project)

    # Distribute images evenly among projects
    images_per_project = len(images) // len(projects) if projects else 0

    sections_html = ""
    for i, project in enumerate(projects):
        start_img = i * images_per_project
        end_img = start_img + images_per_project
        project_images = images[start_img:end_img]

        images_html = ""
        for img in project_images:
            images_html += f'''        <img src="{img}" alt="{project['title']}">\n'''

        sections_html += f'''    <section class="project-section">
      <header class="project-header">
        <h2 class="project-title">{project['title']}</h2>
        <h3 class="project-year">{project['year']}</h3>
      </header>
      <div class="project-gallery">
{images_html}      </div>
    </section>

'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Projects - Maria Goundry Portfolio</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
{generate_nav()}

    <h1>Projects</h1>

{sections_html}

{generate_footer()}
  </div>
</body>
</html>'''

    return html

def generate_photoshoots_html(text_data, images):
    """Generate photoshoots page HTML"""
    print("\n=== Generating PHOTOSHOOTS page ===")

    # Filter out footer items
    content_items = [item for item in text_data if not item['text'].startswith(('EMAIL', 'INSTAGRAM', 'NOT JUST', 'NEIGHBOURHOOD'))]

    # Group photoshoots (h2 year + credits)
    shoots = []
    current_shoot = None

    for item in content_items:
        if item['tag'] == 'h2':
            if current_shoot:
                shoots.append(current_shoot)
            current_shoot = {
                'year': item['text'],
                'credits': []
            }
        elif item['tag'] == 'p' and current_shoot:
            current_shoot['credits'].append(item['text'])

    if current_shoot:
        shoots.append(current_shoot)

    # Distribute images evenly among shoots
    images_per_shoot = len(images) // len(shoots) if shoots else 0

    sections_html = ""
    for i, shoot in enumerate(shoots):
        start_img = i * images_per_shoot
        end_img = start_img + images_per_shoot
        shoot_images = images[start_img:end_img]

        credits_html = ""
        for credit in shoot['credits']:
            credits_html += f'''        <p>{credit}</p>\n'''

        images_html = ""
        for img in shoot_images:
            images_html += f'''        <img src="{img}" alt="Photoshoot {shoot['year']}">\n'''

        sections_html += f'''    <section class="photoshoot-section">
      <header class="photoshoot-header">
        <h2 class="photoshoot-year">{shoot['year']}</h2>
        <div class="photoshoot-credits">
{credits_html}        </div>
      </header>
      <div class="photoshoot-gallery">
{images_html}      </div>
    </section>

'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Photoshoots - Maria Goundry Portfolio</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
{generate_nav()}

    <h1>Photoshoots</h1>

{sections_html}

{generate_footer()}
  </div>
</body>
</html>'''

    return html

def generate_press_html(text_data, images):
    """Generate press page HTML"""
    print("\n=== Generating PRESS page ===")

    # Filter out footer items
    content_items = [item for item in text_data if not item['text'].startswith(('EMAIL', 'INSTAGRAM', 'NOT JUST', 'NEIGHBOURHOOD'))]

    # Group press items (h2 title + p link)
    press_items = []
    current_item = None

    for item in content_items:
        if item['tag'] == 'h2':
            if current_item:
                press_items.append(current_item)
            current_item = {
                'title': item['text'],
                'link': ''
            }
        elif item['tag'] == 'p' and current_item and item['text'].startswith('http'):
            current_item['link'] = item['text']

    if current_item:
        press_items.append(current_item)

    # Distribute images evenly among press items
    images_per_item = len(images) // len(press_items) if press_items else 0

    articles_html = ""
    for i, item in enumerate(press_items):
        start_img = i * images_per_item
        end_img = start_img + images_per_item
        item_images = images[start_img:end_img]

        images_html = ""
        for img in item_images:
            images_html += f'''        <img src="{img}" alt="{item['title']}">\n'''

        articles_html += f'''    <article class="press-item">
      <header class="press-header">
        <h2 class="press-title">{item['title']}</h2>
        <a href="{item['link']}" class="press-link" target="_blank">View Publication</a>
      </header>
      <div class="press-gallery">
{images_html}      </div>
    </article>

'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Press - Maria Goundry Portfolio</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
{generate_nav()}

    <h1>Press</h1>

{articles_html}

{generate_footer()}
  </div>
</body>
</html>'''

    return html

def generate_press_loans_html(text_data, images):
    """Generate press-loans page HTML"""
    print("\n=== Generating PRESS-LOANS page ===")

    # Filter out footer items
    content_items = [item for item in text_data if not item['text'].startswith(('EMAIL', 'INSTAGRAM', 'NOT JUST', 'NEIGHBOURHOOD'))]

    # Extract header
    header_title = "LOOKS AVAILABLE TO BORROW"

    # Group loan items (collect p tags with garment names, then images)
    # For simplicity, we'll create sections with labels + images
    loan_items = []
    current_labels = []

    for item in content_items:
        if item['tag'] == 'h2':
            continue  # Skip header, we already have it
        elif item['tag'] == 'p':
            # These are garment labels
            current_labels.append(item['text'])

    # Create loan items - group every 3-5 labels together
    items_count = max(3, len(images) // 10)  # At least 3 items
    labels_per_item = len(current_labels) // items_count if items_count else 1
    images_per_item = len(images) // items_count if items_count else 1

    for i in range(items_count):
        start_label = i * labels_per_item
        end_label = start_label + labels_per_item
        start_img = i * images_per_item
        end_img = start_img + images_per_item

        loan_items.append({
            'labels': current_labels[start_label:end_label],
            'images': images[start_img:end_img]
        })

    items_html = ""
    for item in loan_items:
        labels_html = ""
        for label in item['labels']:
            labels_html += f'''        <p class="loan-label">{label}</p>\n'''

        images_html = ""
        for img in item['images']:
            images_html += f'''        <img src="{img}" alt="Available garment">\n'''

        items_html += f'''    <article class="loan-item">
      <div class="loan-labels">
{labels_html}      </div>
      <div class="loan-gallery">
{images_html}      </div>
    </article>

'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Press Loans - Maria Goundry Portfolio</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
{generate_nav()}

    <div class="press-loans-header">
      <h1>{header_title}</h1>
    </div>

{items_html}

{generate_footer()}
  </div>
</body>
</html>'''

    return html

def main():
    """Generate all pages"""
    print("=" * 60)
    print("GENERATING CLEAN HTML FOR MARIA GOUNDRY PORTFOLIO")
    print("=" * 60)

    # Load text content
    with open(TEXT_CONTENT_FILE, 'r', encoding='utf-8') as f:
        text_content = json.load(f)

    sections = [
        ('home', 'index.html', generate_home_html),
        ('projects', 'projects.html', generate_projects_html),
        ('photoshoots', 'photoshoots.html', generate_photoshoots_html),
        ('press', 'press.html', generate_press_html),
        ('press-loans', 'press-loans.html', generate_press_loans_html),
    ]

    for section_name, output_filename, generator_func in sections:
        # Extract images from original HTML
        input_html = os.path.join(BASE_INPUT, section_name, 'index.html')
        images = extract_images_from_html(input_html, section_name)

        print(f"\n  Extracted {len(images)} images")

        # Generate HTML
        html = generator_func(text_content[section_name], images)

        # Write to file
        output_file = os.path.join(BASE_OUTPUT, output_filename)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  [OK] Generated {output_filename}")

    print("\n" + "=" * 60)
    print("ALL PAGES GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start local server: python -m http.server 8001")
    print("2. Open http://localhost:8001/ in browser")
    print("3. Test all pages and verify content")
    print("=" * 60)

if __name__ == '__main__':
    main()
