import PyInstaller.__main__
import os
import sys
from data.config import USERNAME  # ✅ import absolu


# Vérifier que PyInstaller est installé
try:
    import PyInstaller
except ImportError:
    print("❌ PyInstaller n'est pas installé! pip install pyinstaller")
    sys.exit(1)

options = [
    'data/gui.py',  # Fichier principal
    f'--name={USERNAME}-TikTokLiveMonitor',  # Nom de l'exe avec username
    '--onefile',
    '--windowed',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=reportlab',
    '--hidden-import=TikTokLive',
    '--hidden-import=tkinter',
    '--hidden-import=PIL',
    '--hidden-import=reportlab.lib',
    '--hidden-import=reportlab.platypus',
    '--hidden-import=reportlab.lib.styles',
    '--hidden-import=reportlab.lib.colors',
    '--hidden-import=reportlab.lib.pagesizes',
    '--hidden-import=reportlab.lib.units',
    '--collect-all=reportlab',
    '--collect-all=TikTokLive',
    '--clean',
]

print(f"🚀 Création de l'exécutable pour l'utilisateur: {USERNAME}...")
print("⏳ Cela peut prendre quelques minutes...\n")

try:
    PyInstaller.__main__.run(options)
    print("\n✅ Exécutable créé avec succès!")
    print(f"📁 Dossier: dist/{USERNAME}-TikTokLiveMonitor.exe")
except Exception as e:
    print(f"\n❌ Erreur lors de la création de l'exécutable: {e}")
    sys.exit(1)
