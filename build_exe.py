"""
Script pour créer un exécutable Windows de l'application TikTok Live Monitor
Utilise PyInstaller pour créer un fichier .exe

Utilisation:
    python build_exe.py
"""
import PyInstaller.__main__
import os
import sys

# Vérifier que PyInstaller est installé
try:
    import PyInstaller
except ImportError:
    print("❌ PyInstaller n'est pas installé!")
    print("Installez-le avec: pip install pyinstaller")
    sys.exit(1)

# Définir les options PyInstaller
# Note: Sur Windows, utilisez ';' pour séparer le chemin source et destination dans --add-data
options = [
    'data/gui.py',  # Fichier principal
    '--name=TikTokLiveMonitor',  # Nom de l'exécutable
    '--onefile',  # Créer un seul fichier exécutable
    '--windowed',  # Masquer la console (pour GUI)
    '--hidden-import=pandas',  # Imports cachés nécessaires
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
    '--collect-all=reportlab',  # Collecter toutes les données de reportlab
    '--collect-all=TikTokLive',  # Collecter toutes les données de TikTokLive
    '--clean',  # Nettoyer les fichiers temporaires avant
]

print("🚀 Démarrage de la création de l'exécutable...")
print("⏳ Cela peut prendre quelques minutes...\n")

# Exécuter PyInstaller
try:
    PyInstaller.__main__.run(options)
    print("\n✅ Exécutable créé avec succès!")
    print("📁 Trouvez-le dans le dossier: dist/TikTokLiveMonitor.exe")
    print("\n💡 Note: L'exécutable peut être signalé par l'antivirus (faux positif courant avec PyInstaller)")
except Exception as e:
    print(f"\n❌ Erreur lors de la création de l'exécutable: {e}")
    sys.exit(1)

