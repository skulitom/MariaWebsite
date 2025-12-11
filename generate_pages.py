#!/usr/bin/env python3
"""
Generate HTML pages for Maria's portfolio website
"""

import os
from pathlib import Path

def get_images_from_folder(folder_path):
    """Get all image files from a folder"""
    images = []
    if os.path.exists(folder_path):
        for file in sorted(os.listdir(folder_path)):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                images.append(file)
    return images

def generate_html_template(page_title, section_name, images, active_page):
    """Generate HTML page template"""

    # Generate image grid HTML
    image_html = []
    for i, img in enumerate(images):
        # Vary grid item sizes for visual interest
        if i % 5 == 0:
            grid_class = "grid-item--two-thirds"
        elif i % 3 == 0:
            grid_class = "grid-item--third"
        else:
            grid_class = "grid-item--half"

        # Vary aspect ratios
        if i % 4 == 0:
            aspect_class = "aspect-1-1"
        elif i % 4 == 1:
            aspect_class = "aspect-3-2"
        elif i % 4 == 2:
            aspect_class = "aspect-2-3"
        else:
            aspect_class = "aspect-3-4"

        image_html.append(f'''        <div class="grid-item {grid_class} {aspect_class}">
          <img src="./images/{section_name}/{img}" alt="Maria Goundry - {page_title}" loading="lazy">
        </div>''')

    images_section = '\n'.join(image_html)

    # Create navigation with active state
    nav_items = {
        'index.html': 'Home',
        'projects.html': 'Projects',
        'photoshoots.html': 'Photoshoots',
        'press.html': 'Press',
        'press-loans.html': 'Press Loans'
    }

    nav_html = []
    for page, label in nav_items.items():
        if page == active_page:
            nav_html.append(f'        <li><a href="{page}" class="active">{label.upper()}</a></li>')
        else:
            nav_html.append(f'        <li><a href="{page}">{label.upper()}</a></li>')

    nav_section = '\n'.join(nav_html)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Maria Goundry - Fashion Designer Portfolio">
  <meta property="og:title" content="Maria Goundry Portfolio - {page_title}">
  <meta property="og:description" content="Fashion design portfolio showcasing projects, photoshoots, and press features">
  <meta property="og:type" content="website">
  <title>{page_title} - Maria Goundry Portfolio</title>

  <!-- CSS -->
  <link rel="stylesheet" href="./css/main.css">
  <link rel="stylesheet" href="./css/layout.css">
  <link rel="stylesheet" href="./css/header.css">
  <link rel="stylesheet" href="./css/footer.css">
  <link rel="stylesheet" href="./css/responsive.css">
</head>
<body class="page-{section_name}">

  <!-- Header -->
  <header class="site-header">
    <nav class="main-nav">
      <a href="index.html" class="site-title">MARIA GOUNDRY PORTFOLIO</a>
      <ul class="nav-links">
{nav_section}
      </ul>
      <button class="mobile-menu-toggle" aria-label="Toggle menu">
        <span class="burger-line"></span>
        <span class="burger-line"></span>
        <span class="burger-line"></span>
      </button>
    </nav>
  </header>

  <!-- Main Content -->
  <main class="main-content">
    <div class="image-grid">
{images_section}
    </div>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4>CONTACT</h4>
        <p><a href="mailto:maria.goundry98@gmail.com">maria.goundry98@gmail.com</a></p>
      </div>
      <div class="footer-section">
        <h4>SOCIAL</h4>
        <p><a href="https://www.instagram.com/mariagoundry/" target="_blank" rel="noopener noreferrer">INSTAGRAM</a></p>
      </div>
      <div class="footer-section">
        <h4>LINKS</h4>
        <p><a href="https://www.notjustalabel.com/maria-goundry" target="_blank" rel="noopener noreferrer">NOT JUST A LABEL</a></p>
        <p><a href="https://www.neighbourhoodmag.com/creative/maria-goundry/" target="_blank" rel="noopener noreferrer">NEIGHBOURHOOD MAGAZINE</a></p>
      </div>
    </div>
    <div class="footer-copyright">
      <p>&copy; {section_name.split('/')[-1].split('\\')[-1].upper()} Maria Goundry. All rights reserved.</p>
    </div>
  </footer>

  <!-- JavaScript -->
  <script src="./js/navigation.js"></script>

</body>
</html>
'''
    return html

def main():
    """Generate all HTML pages"""
    base_path = Path(__file__).parent
    images_path = base_path / 'images'

    pages = [
        ('index.html', 'Home', 'home', 'index.html'),
        ('projects.html', 'Projects', 'projects', 'projects.html'),
        ('photoshoots.html', 'Photoshoots', 'photoshoots', 'photoshoots.html'),
        ('press.html', 'Press', 'press', 'press.html'),
        ('press-loans.html', 'Press Loans', 'press-loans', 'press-loans.html'),
    ]

    for filename, title, section, active_page in pages:
        # Get images for this section
        section_path = images_path / section
        images = get_images_from_folder(section_path)

        print(f"Generating {filename}... ({len(images)} images)")

        # Generate HTML
        html = generate_html_template(title, section, images, active_page)

        # Write to file
        output_path = base_path / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  Created {filename}")

    print(f"\nAll pages generated successfully!")

if __name__ == '__main__':
    main()
