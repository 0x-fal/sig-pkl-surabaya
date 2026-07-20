"""
deploy.py — Script otomatis untuk setup Git dan persiapan deploy ke Streamlit Cloud.
Jalankan: python deploy.py
"""

import os
import subprocess
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def run(cmd, check=True):
    """Run shell command dan print output."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=PROJECT_DIR, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if result.returncode != 0 and check:
        if result.stderr.strip():
            print(f"    ERROR: {result.stderr.strip()}")
        return False
    return True


def create_gitignore():
    """Buat .gitignore file."""
    gitignore = """# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
venv/
.venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Streamlit
.streamlit/secrets.toml
"""
    path = os.path.join(PROJECT_DIR, ".gitignore")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(gitignore)
        print("  Created .gitignore")
    else:
        print("  .gitignore already exists")


def main():
    print("=" * 60)
    print("  DEPLOY SCRIPT — Persiapan GitHub + Streamlit Cloud")
    print("=" * 60)

    # Step 1: Create .gitignore
    print("\n[1/4] Creating .gitignore...")
    create_gitignore()

    # Step 2: Init git
    print("\n[2/4] Initializing Git...")
    if os.path.exists(os.path.join(PROJECT_DIR, ".git")):
        print("  Git already initialized")
    else:
        run("git init")

    # Step 3: Add & commit
    print("\n[3/4] Adding files & committing...")
    run("git add .")
    run('git commit -m "Peta Interaktif Keadilan Spasial PKL Surabaya - Initial commit"')

    # Step 4: Instructions
    print("\n[4/4] LANGKAH SELANJUTNYA (Manual):")
    print("=" * 60)
    print("""
  STEP A — Buat GitHub Repository:
  1. Buka https://github.com/new
  2. Repository name: sig-pkl-surabaya
  3. Visibility: PUBLIC (wajib untuk Streamlit Cloud gratis)
  4. Jangan centang "Add README" (sudah ada)
  5. Klik "Create repository"

  STEP B — Push ke GitHub:
  Jalankan perintah ini di terminal:

    git remote add origin https://github.com/USERNAME/sig-pkl-surabaya.git
    git branch -M main
    git push -u origin main

  (Ganti USERNAME dengan username GitHub kamu)

  STEP C — Deploy ke Streamlit Cloud:
  1. Buka https://share.streamlit.io
  2. Login dengan akun GitHub
  3. Klik "New app"
  4. Repository: USERNAME/sig-pkl-surabaya
  5. Branch: main
  6. Main file path: app.py
  7. Klik "Deploy!"
  8. Tunggu ~2 menit
  9. SELESAI! URL kamu: https://sig-pkl-surabaya.streamlit.app

  STEP D — Copy URL ke Laporan:
  Paste Live URL ke bagian "Live URL" di LAPORAN.md
""")
    print("=" * 60)
    print("  Script selesai. Lanjutkan dengan STEP A di atas.")


if __name__ == "__main__":
    main()
