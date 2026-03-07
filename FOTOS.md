# Protocol per afegir fotos noves a holcat.com

## On posar les fotos

### Fotos de projectes → `img/projects/<categoria>/`

Posa la foto a la subcarpeta que correspongui al tipus de feina:

| Carpeta | Servei web | Exemples |
|---|---|---|
| `img/projects/kitchen/` | Keukens | cuines renovades |
| `img/projects/bathroom/` | Badkamers | banys renovats |
| `img/projects/living/` | Woonruimtes | salons, habitacions |
| `img/projects/outdoor/` | Buiten & Schuren | exterior, tanques, coberts |
| `img/projects/painting/` | Schilderen & Afwerking | pintura, acabats |
| `img/projects/maintenance/` | Onderhoud & Reparatie | manteniment, reparacions |

**Per què importa la carpeta?**
- Apareixerà automàticament al visor (lightbox) ✓
- S'associarà a la categoria correcta del servei ✓
- Quan es cliqui "Badkamers" a la web, si hi ha 3 fotos de banys en triarà una aleatòria ✓

### Fotos de l'equip → `img/team/`
Fotos de treballadors o l'equip. NO apareixeran al visor lightbox ni als serveis.

---

## Com afegir-les (3 passos)

1. **Copia la foto** a la carpeta correcta (des del Finder)
2. **Escriu a Claude**: "He afegit fotos noves, actualitza la web"
3. **Claude fa la resta**: comprimir, afegir a la web, push automàtic

---

## Consells per les fotos

- Format: `.jpg` preferiblement
- Nom: sense espais ni accents → `bany-wageningen-2.jpg`
- Mida original: qualsevol (es comprimen automàticament a màx 1600px)
- Orientació: horitzontal funciona millor per la galeria principal

---

## Fotos actuals a la web (afegides manualment)

### Galeria principal (lightbox activat)
| Fitxer | Categoria |
|---|---|
| `img/project-kitchen.jpg` | kitchen |
| `img/project-bathroom.jpg` | bathroom |
| `img/project-room.jpg` | living |
| `img/project-bedroom.jpg` | living |
| `img/project-roof.jpg` | maintenance |
| `img/project-fence-2.jpg` | outdoor |
| `img/project-painting-room.jpg` | painting |

### Galeria de marca (sense lightbox)
| Fitxer | Nota |
|---|---|
| `img/project-fence-1.jpg` | treballador a la tanca |
| `img/hero-process.jpg` | foto en acció |
| `img/process-team.jpg` | foto equip |

### Altres
| Fitxer | Secció |
|---|---|
| `img/magnolia.jpg` | Hero (fons) |
| `img/wageningen.jpg` | About (foto Wageningen) |
