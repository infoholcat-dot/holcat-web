#!/usr/bin/env python3
"""
Script per afegir fotos noves de img/projects/ a la galeria de holcat.com
Ús: python3 afegir-fotos.py
"""

import os
import re
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(PROJECT_DIR, 'index.html')
PROJECTS_DIR = os.path.join(PROJECT_DIR, 'img', 'projects')
TEAM_DIR = os.path.join(PROJECT_DIR, 'img', 'team')

EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')

def get_html():
    with open(HTML_FILE, 'r') as f:
        return f.read()

def save_html(content):
    with open(HTML_FILE, 'w') as f:
        f.write(content)

def compress_photo(path):
    """Comprimeix la foto a màxim 1600px i qualitat 82 amb sips (macOS)"""
    size = os.path.getsize(path)
    if size > 800_000:  # >800KB
        print(f"  Comprimint {os.path.basename(path)} ({size//1024}KB)...")
        subprocess.run([
            'sips', '-Z', '1600',
            '--setProperty', 'formatOptions', '82',
            path
        ], capture_output=True)
        new_size = os.path.getsize(path)
        print(f"  -> {new_size//1024}KB")
    else:
        print(f"  {os.path.basename(path)} ja es prou petita ({size//1024}KB), no cal comprimir")

def find_new_project_photos(content):
    """Retorna fotos de img/projects/ que encara no són a l'HTML"""
    if not os.path.exists(PROJECTS_DIR):
        return []

    all_photos = [
        f for f in os.listdir(PROJECTS_DIR)
        if f.lower().endswith(EXTENSIONS)
    ]

    new_photos = []
    for photo in sorted(all_photos):
        if f'img/projects/{photo}' not in content:
            new_photos.append(photo)

    return new_photos

def find_new_team_photos(content):
    """Retorna fotos de img/team/ que encara no són a l'HTML"""
    if not os.path.exists(TEAM_DIR):
        return []

    all_photos = [
        f for f in os.listdir(TEAM_DIR)
        if f.lower().endswith(EXTENSIONS)
    ]

    new_photos = []
    for photo in sorted(all_photos):
        if f'img/team/{photo}' not in content:
            new_photos.append(photo)

    return new_photos

def add_project_photo(content, photo):
    """Afegeix una foto de projecte a la gallery-grid amb lightbox"""
    img_tag = f'''        <div class="gallery-item reveal">
          <img src="img/projects/{photo}" data-lightbox alt="Projecte HolCat">
        </div>'''

    # Insereix abans del tancament de gallery-grid
    content = content.replace(
        '      </div>\n      <div class="gallery-brand">',
        img_tag + '\n      </div>\n      <div class="gallery-brand">'
    )
    return content

def add_team_photo(content, photo):
    """Afegeix una foto d'equip a la galeria brand (sense lightbox)"""
    img_tag = f'''        <div class="gallery-brand-item gallery-brand-half reveal">
          <img src="img/team/{photo}" alt="Equip HolCat">
        </div>'''

    # Insereix al final de gallery-brand, abans del tancament
    content = content.replace(
        '      </div>\n    </div>\n  </section>\n\n  <section class="promise"',
        img_tag + '\n      </div>\n    </div>\n  </section>\n\n  <section class="promise"'
    )
    return content

def main():
    print("=== HolCat - Afegir fotos noves ===\n")

    content = get_html()

    # Fotos de projectes noves
    new_projects = find_new_project_photos(content)
    if new_projects:
        print(f"Fotos de projectes noves trobades: {len(new_projects)}")
        for photo in new_projects:
            path = os.path.join(PROJECTS_DIR, photo)
            print(f"\n  + {photo}")
            compress_photo(path)
            content = add_project_photo(content, photo)
        print()
    else:
        print("Cap foto de projecte nova a img/projects/\n")

    # Fotos d'equip noves
    new_team = find_new_team_photos(content)
    if new_team:
        print(f"Fotos d'equip noves trobades: {len(new_team)}")
        for photo in new_team:
            path = os.path.join(TEAM_DIR, photo)
            print(f"\n  + {photo}")
            compress_photo(path)
            content = add_team_photo(content, photo)
        print()
    else:
        print("Cap foto d'equip nova a img/team/\n")

    if not new_projects and not new_team:
        print("No hi ha res a fer.")
        return

    save_html(content)
    print("index.html actualitzat.")

    # Git commit + push
    total = len(new_projects) + len(new_team)
    names = ', '.join(new_projects + new_team)
    commit_msg = f"Add {total} new photo(s): {names}\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

    subprocess.run(['git', 'add', '-A'], cwd=PROJECT_DIR)
    subprocess.run(['git', 'commit', '-m', commit_msg], cwd=PROJECT_DIR)
    subprocess.run(['git', 'push'], cwd=PROJECT_DIR)
    print("\nPush fet! Les fotos apareixeran a holcat.com en 1-2 minuts.")

if __name__ == '__main__':
    main()
