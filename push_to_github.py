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
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR)

    run(["gh", "repo", "clone", REPO, TMP_DIR, "--", "--depth", "1"])

    for f in FILES_TO_PUSH:
        src = os.path.join(SOURCE_DIR, f)
        if os.path.exists(src):
            shutil.copy2(src, TMP_DIR)
        else:
            print(f"⚠️ Fichier manquant : {src}")

    run(["git", "config", "user.name", "Jimmy Sambin"], cwd=TMP_DIR)
    run(["git", "config", "user.email", "j.sambin@gmail.com"], cwd=TMP_DIR)

    run(["git", "add", "-A"], cwd=TMP_DIR)
    run(["git", "commit", "-m", COMMIT_MSG], cwd=TMP_DIR)
    run(["git", "push", "origin", "main"], cwd=TMP_DIR)

    shutil.rmtree(TMP_DIR)
    print("✅ Push terminé avec succès")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        sys.exit(1)
