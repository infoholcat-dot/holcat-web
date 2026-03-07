# Protocol per afegir fotos noves a holcat.com

## On posar les fotos

### Fotos de projectes → `img/projects/`
Qualsevol foto d'una feina realitzada:
- Cuines, banys, salons, habitacions
- Pintura, fusteria, tanca, teulada...
- Apareixeran a la galeria amb visor (lightbox)

### Fotos de l'equip → `img/team/`
Fotos de les persones:
- Treballadors en acció
- Foto d'equip
- NO apareixeran al visor lightbox

---

## Com afegir-les (passos)

1. Copia la foto/es a la carpeta corresponent (`img/projects/` o `img/team/`)
2. Escriu a Claude: "He afegit fotos noves, actualitza la web"
3. Claude comprimirà les fotos, les afegirà a la web i farà el push automàticament

---

## Consells per les fotos

- Format: `.jpg` preferiblement (també `.png`)
- Nom del fitxer: sense espais ni accents. Usa guions: `cuina-wageningen.jpg`
- Mida original: qualsevol (Claude les comprimeix automàticament)
- Orientació: horitzontal funciona millor per la galeria principal

---

## Fotos actuals a la web

### Galeria de projectes (amb lightbox)
| Fitxer | Secció |
|---|---|
| `img/project-kitchen.jpg` | Galeria principal |
| `img/project-bathroom.jpg` | Galeria principal |
| `img/project-room.jpg` | Galeria principal |
| `img/project-bedroom.jpg` | Galeria principal |
| `img/project-roof.jpg` | Galeria principal |
| `img/project-fence-2.jpg` | Galeria brand (tanca) |
| `img/project-painting-room.jpg` | Galeria brand (menjador) |

### Fotos de marca / persones (sense lightbox)
| Fitxer | Secció |
|---|---|
| `img/project-fence-1.jpg` | Galeria brand (treballador) |
| `img/hero-process.jpg` | Galeria brand (en acció) |
| `img/process-team.jpg` | Galeria brand (equip) |
| `img/magnolia.jpg` | Hero (fons) |
| `img/wageningen.jpg` | About |
