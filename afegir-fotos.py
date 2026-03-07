#!/usr/bin/env python3
"""
Script per afegir fotos noves a holcat.com
Ús: python3 afegir-fotos.py

Estructura de carpetes:
  img/projects/kitchen/      → Keukens (cuines)
  img/projects/bathroom/     → Badkamers (banys)
  img/projects/living/       → Woonruimtes (salons, habitacions)
  img/projects/outdoor/      → Buiten & Schuren (exterior, tanca)
  img/projects/painting/     → Schilderen & Afwerking (pintura)
  img/projects/maintenance/  → Onderhoud & Reparatie (manteniment)
  img/team/                  → Fotos de l'equip (sense lightbox ni categoria)
"""

import os
import re
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE   = os.path.join(PROJECT_DIR, 'index.html')

CATEGORIES = ['kitchen', 'bathroom', 'living', 'outdoor', 'painting', 'maintenance']
EXTENSIONS  = ('.jpg', '.jpeg', '.png', '.webp')
TEAM_DIR    = os.path.join(PROJECT_DIR, 'img', 'team')


def get_html():
    with open(HTML_FILE, 'r') as f:
        return f.read()

def save_html(content):
    with open(HTML_FILE, 'w') as f:
        f.write(content)

def compress_photo(path):
    """Comprimeix la foto a màxim 1600px i qualitat 82 amb sips (macOS)"""
    size = os.path.getsize(path)
    if size > 800_000:
        print(f"    Comprimint ({size//1024}KB)...")
        subprocess.run(
            ['sips', '-Z', '1600', '--setProperty', 'formatOptions', '82', path],
            capture_output=True
        )
        print(f"    → {os.path.getsize(path)//1024}KB")
    else:
        print(f"    Ja és prou petita ({size//1024}KB)")

def find_new_photos(content):
    """
    Retorna llista de (path, categoria) de fotos noves no presents a l'HTML.
    Escaneja img/projects/<categoria>/ i img/team/
    """
    new = []

    # Project categories
    for cat in CATEGORIES:
        folder = os.path.join(PROJECT_DIR, 'img', 'projects', cat)
        if not os.path.exists(folder):
            continue
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith(EXTENSIONS):
                rel = f'img/projects/{cat}/{f}'
                if rel not in content:
                    new.append((os.path.join(folder, f), rel, cat))

    # Team photos
    if os.path.exists(TEAM_DIR):
        for f in sorted(os.listdir(TEAM_DIR)):
            if f.lower().endswith(EXTENSIONS):
                rel = f'img/team/{f}'
                if rel not in content:
                    new.append((os.path.join(TEAM_DIR, f), rel, 'team'))

    return new

def add_project_photo(content, rel_path, category):
    """Afegeix foto de projecte a gallery-grid amb data-lightbox i data-category"""
    img_tag = (
        f'        <div class="gallery-item reveal" data-category="{category}">\n'
        f'          <img src="{rel_path}" data-lightbox alt="Projecte HolCat">\n'
        f'        </div>'
    )
    content = content.replace(
        '      </div>\n      <div class="gallery-brand">',
        img_tag + '\n      </div>\n      <div class="gallery-brand">'
    )
    return content

def add_team_photo(content, rel_path):
    """Afegeix foto d'equip a gallery-brand (sense lightbox ni categoria)"""
    img_tag = (
        f'        <div class="gallery-brand-item gallery-brand-half reveal">\n'
        f'          <img src="{rel_path}" alt="Equip HolCat">\n'
        f'        </div>'
    )
    content = content.replace(
        '      </div>\n    </div>\n  </section>\n\n  <section class="promise"',
        img_tag + '\n      </div>\n    </div>\n  </section>\n\n  <section class="promise"'
    )
    return content

def main():
    print("=== HolCat - Afegir fotos noves ===\n")

    content  = get_html()
    new_all  = find_new_photos(content)

    if not new_all:
        print("Cap foto nova trobada a img/projects/ ni img/team/")
        print("\nRecorda l'estructura de carpetes:")
        for cat in CATEGORIES:
            print(f"  img/projects/{cat}/")
        print("  img/team/")
        return

    added = []
    for path, rel, category in new_all:
        name = os.path.basename(path)
        print(f"+ {name}  [{category}]")
        compress_photo(path)

        if category == 'team':
            content = add_team_photo(content, rel)
        else:
            content = add_project_photo(content, rel, category)

        added.append(name)

    save_html(content)
    print(f"\nindex.html actualitzat amb {len(added)} foto(s).")

    names      = ', '.join(added)
    commit_msg = (
        f"Add {len(added)} photo(s): {names}\n\n"
        f"Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    )
    subprocess.run(['git', 'add', '-A'], cwd=PROJECT_DIR)
    subprocess.run(['git', 'commit', '-m', commit_msg], cwd=PROJECT_DIR)
    subprocess.run(['git', 'push'], cwd=PROJECT_DIR)
    print("Push fet! Apareixerà a holcat.com en 1-2 minuts.")

if __name__ == '__main__':
    main()
