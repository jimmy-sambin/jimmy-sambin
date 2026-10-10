# Runbook — Mise à jour du compte GitHub via gh + git

## Objectif

Ce document centralise les commandes, scripts et procédures utilisés pour se connecter à GitHub, mettre à jour le profil `jimmy-sambin` et pousser des fichiers sur n'importe quel dépôt.

Il permet à un LLM (ou à l'utilisateur) de reprendre rapidement les opérations sans rechercher les commandes.

---

## Prérequis

- **Git** installé (vient avec Git for Windows)
- **CLI GitHub (`gh`)** installée : https://cli.github.com/
- Un compte GitHub existant (`jimmy-sambin`)
- Un token `gh` valide (authentification via navigateur ou token)

---

## 1. Vérifier l'authentification GitHub

### Bash / PowerShell

```bash
gh auth status
```

Résultat attendu :

```text
github.com
  ✓ Logged in to github.com account jimmy-sambin
  - Active account: true
```

### Si non connecté

```bash
gh auth login
```

Suivre les instructions (HTTPS + navigateur ou token).

---

## 2. Configurer git pour utiliser l'authentification `gh`

GitHub refuse l'authentification par mot de passe. Il faut que `git` utilise le token `gh`.

```bash
gh auth setup-git
```

---

## 3. Pousser des fichiers sur un dépôt existant

### 3.1 Méthode rapide : cloner en profondeur 1, copier, commiter, pousser

```bash
# Variables
REPO="jimmy-sambin/jimmy-sambin"
TMP_DIR="C:/dll/GITHUB-PRO/jimmy-sambin-tmp"
SOURCE_DIR="C:/dll/GITHUB-PRO"

# Nettoyage + création du dossier temporaire
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

# Clonage
gh repo clone "$REPO" "$TMP_DIR" -- --depth 1
# ou
git clone --depth 1 "https://github.com/$REPO.git" "$TMP_DIR"

# Copie des fichiers à mettre à jour
cp "$SOURCE_DIR/README.md" "$TMP_DIR/"
cp "$SOURCE_DIR/banner.png" "$TMP_DIR/"
cp "$SOURCE_DIR/logo.png" "$TMP_DIR/"
cp "$SOURCE_DIR/logo-avatar.png" "$TMP_DIR/"

# Configuration git
cd "$TMP_DIR"
git config user.name "Jimmy Sambin"
git config user.email "j.sambin@gmail.com"

# Commit + push
git add -A
git commit -m "feat: mise à jour des assets du profil GitHub

Co-Authored-By: Claude Code <noreply@anthropic.com>"
git push origin main

# Nettoyage
cd ..
rm -rf "$TMP_DIR"
```

### 3.2 Méthode `gh repo clone` + push

```bash
gh repo clone jimmy-sambin/jimmy-sambin C:/dll/GITHUB-PRO/jimmy-sambin-tmp
cd C:/dll/GITHUB-PRO/jimmy-sambin-tmp

# Modifier/copier les fichiers...

git add -A
git commit -m "chore: mise à jour des assets"
git push origin main
```

---

## 4. Créer un nouveau dépôt (si besoin)

### Via `gh`

```bash
gh repo create mon-nouveau-projet --public --description "Description du projet" --source=.
```

### Puis pousser

```bash
git init
git add -A
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/jimmy-sambin/mon-nouveau-projet.git
git push -u origin main
```

---

## 5. Vérifier le dépôt distant

```bash
gh repo view jimmy-sambin/jimmy-sambin --json name,owner,url,pushedAt,viewerPermission,visibility,isEmpty
```

---

## 6. Problèmes courants

### `fatal: Authentication failed for 'https://github.com/...'`

Causé par l'absence de `gh auth setup-git`. Solution :

```bash
gh auth setup-git
```

### `remote: Invalid username or token. Password authentication is not supported`

Pareil : authentification non configurée. Lancer :

```bash
gh auth login
gh auth setup-git
```

### Dossier temporaire non nettoyé

```bash
rm -rf "C:/dll/GITHUB-PRO/jimmy-sambin-tmp"
```

### Branche par défaut non nommée `main`

```bash
git branch -M main
```

---

## 7. Script Python générique de push

Script utilisable pour n'importe quel dépôt.

### Fichier : `C:/dll/GITHUB-PRO/push_to_github.py`

```python
import subprocess
import shutil
import os
import sys

REPO = "jimmy-sambin/jimmy-sambin"
SOURCE_DIR = r"C:\dll\GITHUB-PRO"
TMP_DIR = os.path.join(SOURCE_DIR, "jimmy-sambin-tmp")
FILES_TO_PUSH = ["README.md", "banner.png", "logo.png", "logo-avatar.png"]
COMMIT_MSG = "feat: mise à jour automatique des assets du profil GitHub"


def run(cmd, cwd=None):
    print(f"> {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), check=True)
    return result


def main():
    # Nettoyage
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR)

    # Clonage
    run(["gh", "repo", "clone", REPO, TMP_DIR, "--", "--depth", "1"])

    # Copie des fichiers
    for f in FILES_TO_PUSH:
        src = os.path.join(SOURCE_DIR, f)
        if os.path.exists(src):
            shutil.copy2(src, TMP_DIR)
        else:
            print(f"⚠️ Fichier manquant : {src}")

    # Config git
    run(["git", "config", "user.name", "Jimmy Sambin"], cwd=TMP_DIR)
    run(["git", "config", "user.email", "j.sambin@gmail.com"], cwd=TMP_DIR)

    # Commit + push
    run(["git", "add", "-A"], cwd=TMP_DIR)
    run(["git", "commit", "-m", COMMIT_MSG], cwd=TMP_DIR)
    run(["git", "push", "origin", "main"], cwd=TMP_DIR)

    # Nettoyage
    shutil.rmtree(TMP_DIR)
    print("✅ Push terminé avec succès")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        sys.exit(1)
```

### Utilisation

```bash
python "C:\dll\GITHUB-PRO\push_to_github.py"
```

---

## 8. Commandes PowerShell équivalentes

### Vérifier `gh`

```powershell
gh auth status
```

### Configurer git

```powershell
gh auth setup-git
```

### Cloner, modifier, pousser

```powershell
$repo = "jimmy-sambin/jimmy-sambin"
$tmp = "C:\dll\GITHUB-PRO\jimmy-sambin-tmp"
$source = "C:\dll\GITHUB-PRO"

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $tmp
New-Item -ItemType Directory -Path $tmp | Out-Null

gh repo clone $repo $tmp -- --depth 1

Copy-Item "$source\README.md" $tmp
Copy-Item "$source\banner.png" $tmp
Copy-Item "$source\logo.png" $tmp
Copy-Item "$source\logo-avatar.png" $tmp

Set-Location $tmp
git config user.name "Jimmy Sambin"
git config user.email "j.sambin@gmail.com"

git add -A
git commit -m "feat: mise à jour des assets du profil GitHub`

Co-Authored-By: Claude Code <noreply@anthropic.com>"
git push origin main

Set-Location ..
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $tmp
```

---

## 9. Historique des commits réalisés

| Hash | Message | Date |
|------|---------|------|
| `5d86180` | feat: ajout du bandeau, du logo et du README de profil GitHub | 2026-10-10 |
| `b9263da` | fix: mise à jour de l'email de contact dans le README | 2026-10-10 |
| `2075b7c` | feat: ajout de l'avatar rond transparent | 2026-10-10 |

---

## 10. Liens utiles

- Profil GitHub : https://github.com/jimmy-sambin
- Dépôt du profil : https://github.com/jimmy-sambin/jimmy-sambin
- README : https://github.com/jimmy-sambin/jimmy-sambin/blob/main/README.md
- Avatar : https://github.com/jimmy-sambin/jimmy-sambin/blob/main/logo-avatar.png
- Documentation `gh` : https://cli.github.com/manual/
