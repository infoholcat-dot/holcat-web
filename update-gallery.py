#!/usr/bin/env python3
"""
HolCat Gallery Updater
Ús: python3 update-gallery.py

Escaneig img/projects/ i reconstrueix la galeria a index.html.
Estructura de carpetes:
  img/projects/kitchen/    → fotos de cuines
  img/projects/bathroom/   → fotos de banys
  img/projects/living/     → fotos de salons/habitacions
  img/projects/outdoor/    → fotos d'exterior
  img/projects/painting/   → fotos de pintura
  img/projects/maintenance/ → fotos de manteniment

Layout automàtic:
  - 1a foto: gran (2 columnes)
  - Fotos centrals: 1 columna
  - Última foto sola en fila: ample complet (3 columnes)
"""

import os
import re

PROJECTS_DIR = "img/projects"
HTML_FILE = "index.html"

CATEGORY_ORDER = ["kitchen", "bathroom", "living", "outdoor", "painting", "maintenance"]

CATEGORY_LABELS = {
    "kitchen":     "Keukenrenovatie",
    "bathroom":    "Badkamerrenovatie",
    "living":      "Woonruimte",
    "outdoor":     "Buitenwerk",
    "painting":    "Schilderwerk",
    "maintenance": "Onderhoud",
}

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')


def get_all_photos():
    photos = []
    for category in CATEGORY_ORDER:
        cat_path = os.path.join(PROJECTS_DIR, category)
        if not os.path.isdir(cat_path):
            continue
        files = sorted(f for f in os.listdir(cat_path) if f.lower().endswith(IMAGE_EXTENSIONS))
        for f in files:
            photos.append({
                "src": f"{PROJECTS_DIR}/{category}/{f}",
                "category": category,
                "alt": CATEGORY_LABELS.get(category, category.capitalize()),
            })
    return photos


def last_item_is_alone(n):
    """
    Grid 3 columnes, 1a foto ocupa 2 columnes:
    Fila 1: item[0](span2) + item[1](span1) = 3 cel·les
    Files 2+: 3 items per fila
    L'últim queda sol si (n-2) % 3 == 1
    """
    if n <= 1:
        return False
    return (n - 2) % 3 == 1


def build_gallery_grid(photos):
    n = len(photos)
    delays = ["", "d1", "d2", "d3", "d4", "d5"]
    lines = ['      <div class="gallery-grid">']

    for i, photo in enumerate(photos):
        delay = delays[i % len(delays)]
        css = "gallery-item reveal"
        if delay:
            css += f" {delay}"
        if i == 0:
            css += " gallery-item-first"
        elif i == n - 1 and last_item_is_alone(n):
            css += " gallery-item-wide"

        lines.append(f'        <div class="{css}" data-category="{photo["category"]}">')
        lines.append(f'          <img src="{photo["src"]}" data-lightbox alt="{photo["alt"]}">')
        lines.append(f'        </div>')

    lines.append('      </div>')
    return "\n".join(lines)


def update_html(new_grid_html):
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'      <div class="gallery-grid">.*?      </div>'
    new_content = re.sub(pattern, new_grid_html, content, flags=re.DOTALL)

    if new_content == content:
        print("ERROR: No s'ha trobat la secció gallery-grid al HTML.")
        return False

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def main():
    if not os.path.exists(HTML_FILE):
        print(f"ERROR: No es troba {HTML_FILE}. Executa el script des de la carpeta holcat-web.")
        return

    photos = get_all_photos()

    if not photos:
        print("No s'han trobat fotos a img/projects/")
        return

    print(f"Fotos trobades: {len(photos)}")
    for p in photos:
        print(f"  [{p['category']:12}] {p['src']}")

    new_grid = build_gallery_grid(photos)

    if update_html(new_grid):
        print(f"\n✓ Galeria actualitzada amb {len(photos)} fotos.")
        print("  Obra el index.html al navegador per verificar.")
    else:
        print("\n✗ Error actualitzant el HTML.")


if __name__ == "__main__":
    main()
