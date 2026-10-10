# Runbook — Création du logo et du bandeau GitHub

## Objectif

Ce document centralise la création des assets visuels pour le profil GitHub de Jimmy Sambin : logo, bandeau, avatar rond, et conversion SVG → PNG.

Il permet à un LLM (ou à l'utilisateur) de reproduire, modifier ou regénérer ces assets plus tard.

---

## 1. Spécifications finales

| Asset | Fichier | Dimensions | Format | Fond |
|-------|---------|------------|--------|------|
| Logo standard | `logo.svg` / `logo.png` | 512×512 | SVG + PNG | Bleu foncé `#0f172a` |
| Bandeau | `banner.svg` / `banner.png` | 1280×420 | SVG + PNG | Bleu foncé dégradé |
| Avatar | `logo-avatar.svg` / `logo-avatar.png` | 512×512 | SVG + PNG | **Transparent** + rond |

Palette :

- Fond : `#020617`, `#0f172a`, `#1e293b`
- Accent cyan/bleu : `#06b6d4`, `#22d3ee`, `#3b82f6`, `#60a5fa`
- Texte : `#f8fafc`, `#94a3b8`, `#64748b`

---

## 2. Logo standard (`logo.svg`)

### Description visuelle

- Cercle extérieur bleu foncé
- Anneaux de circuit en cyan/bleu
- Bouclier hexagonal au centre (cybersécurité)
- Nœud central avec connexions (réseau/OT)
- Motifs industriels en bas (BACnet/KNX/GTB)
- Initiales **JS** en bas

### Fichier source

```
C:\dll\GITHUB-PRO\logo.svg
```

### Commande pour convertir le logo en PNG

Le logo SVG utilise des dégradés et des effets qui ne passent pas bien avec `svglib`/`reportlab`. Utiliser **Edge en mode headless** pour un rendu fidèle.

---

## 3. Bandeau (`banner.svg`)

### Description visuelle

- Fond dégradé bleu nuit
- Grille subtile
- Nom **Jimmy SAMBIN** en gros
- Tagline : `Ingénierie · MLOps · IA appliquée · Data/OT`
- Badges : Cybersecurity, Applied AI, GTB/OT, Python/R
- Liens GitHub + LinkedIn
- Logo réduit à droite

### Fichier source

```
C:\dll\GITHUB-PRO\banner.svg
```

---

## 4. Avatar rond transparent (`logo-avatar.svg`)

### Particularités

- Fond transparent via `mask` circulaire
- Pas de bordure carrée visible
- Même design que le logo standard mais inscrit dans un cercle

### Fichier source

```
C:\dll\GITHUB-PRO\logo-avatar.svg
```

---

## 5. Conversion SVG → PNG avec Microsoft Edge headless

### Pourquoi Edge headless ?

Les bibliothèques Python (`cairosvg`, `svglib`) ont échoué :

- `cairosvg` nécessite la DLL Cairo (non présente)
- `svglib/reportlab` ne gère pas bien les dégradés SVG et filtres

Microsoft Edge headless rend les SVG avec le moteur Chromium, donc résultat fidèle.

### Prérequis

- Microsoft Edge installé (chemin par défaut ci-dessous)
- Python 3 + PIL/Pillow (pour recadrage et masque alpha)

### Script Python de conversion

Fichier : `C:/dll/GITHUB-PRO/svg_to_png_edge.py`

```python
import subprocess
import os
import tempfile
import shutil
from PIL import Image, ImageDraw

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT_DIR = r"C:\dll\GITHUB-PRO"


def render_svg(svg_name, png_name, width, height, transparent=False, circular=False):
    svg_path = os.path.join(OUT_DIR, svg_name)
    png_path = os.path.join(OUT_DIR, png_name)

    with open(svg_path, "r", encoding="utf-8") as f:
        svg_data = f.read()

    if transparent:
        bg = "transparent"
    else:
        bg = "#020617"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body{{margin:0;padding:0;background:{bg};overflow:hidden;}}</style>
</head><body>{svg_data}</body></html>"""

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html)
        tmp_html = tmp.name

    udd = os.path.join(tempfile.gettempdir(), f"udd_{png_name}")

    cmd = [
        EDGE,
        "--headless",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-background-timer-throttling",
        "--hide-scrollbars",
        "--window-size", f"{width},{height}",
        "--user-data-dir", udd,
        "--screenshot", png_path,
        "file:///" + tmp_html.replace("\\", "/")
    ]

    print(f"Rendering {png_name}...")
    subprocess.run(cmd, check=True)

    # Post-traitement
    with Image.open(png_path) as img:
        if circular:
            img = img.convert("RGBA")
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, width - 1, height - 1), fill=255)
            out = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            out.paste(img, (0, 0), mask)
            out.save(png_path)
        else:
            img = img.convert("RGB")
            img.save(png_path)

    shutil.rmtree(udd, ignore_errors=True)
    os.unlink(tmp_html)

    size_kb = os.path.getsize(png_path) / 1024
    print(f"Saved: {png_path} ({size_kb:.1f} Ko)")


def main():
    render_svg("banner.svg", "banner.png", 1280, 420, transparent=False)
    render_svg("logo.svg", "logo.png", 512, 512, transparent=False)
    render_svg("logo-avatar.svg", "logo-avatar.png", 512, 512, transparent=True, circular=True)


if __name__ == "__main__":
    main()
```

### Utilisation

```bash
python "C:\dll\GITHUB-PRO\svg_to_png_edge.py"
```

---

## 6. Commandes PowerShell équivalentes

### Vérifier la présence d'Edge

```powershell
Test-Path "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

### Lancer un rendu simple

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$tmp = New-TemporaryFile
$tmpHtml = "$($tmp.FullName).html"
Set-Content -Path $tmpHtml -Value "<!DOCTYPE html><body style='margin:0;background:#020617;'>$([IO.File]::ReadAllText('C:\dll\GITHUB-PRO\banner.svg'))</body></html>"
$out = "C:\dll\GITHUB-PRO\banner.png"
& $edge "--headless" "--disable-gpu" "--hide-scrollbars" "--window-size=1280,420" "--screenshot=$out" "file:///$($tmpHtml -replace '\\','/')"
Remove-Item $tmpHtml
```

---

## 7. Tests et vérifications

### Vérifier la taille d'un PNG

```bash
python -c "from PIL import Image; img = Image.open('C:/dll/GITHUB-PRO/banner.png'); print(img.size, img.mode)"
```

### Lister les assets

```bash
ls -lh C:/dll/GITHUB-PRO/*.png
```

### Vérifier le rendu du README en local

Ouvrir :

```
C:\dll\GITHUB-PRO\preview.html
```

---

## 8. Mise à jour du README après modification des assets

Le README doit référencer les versions PNG (pas SVG) pour éviter les problèmes de cache GitHub.

### Extrait du README

```markdown
<p align="center">
  <img src="banner.png" alt="Jimmy Sambin — RSI, cybersécurité, IA appliquée, GTB/OT" width="100%" />
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/sambin-jimmy-rsi" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="mailto:j.sambin@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
</p>
```

---

## 9. Liens entre les runbooks

- Pour la mise à jour GitHub (push, auth, commandes) : voir `GITHUB-UPDATE-RUNBOOK.md`
- Ce fichier concerne uniquement la création graphique des assets.

---

## 10. Notes pour reproduction future

- Toujours garder les fichiers `.svg` comme sources maîtresses.
- Convertir en `.png` juste avant le push.
- Utiliser Edge headless pour un rendu correct des dégradés et du glow.
- Pour un avatar : activer `transparent=True` + `circular=True`.
- Ne pas utiliser `cairosvg` sans installer Cairo au préalable.
- Le badge Email pointe vers `j.sambin@gmail.com`.
