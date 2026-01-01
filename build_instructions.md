# Instructions pour créer un exécutable Windows

## Prérequis

1. Installer PyInstaller :
```bash
pip install pyinstaller
```

2. S'assurer que toutes les dépendances sont installées :
```bash
cd data
pip install -r requirements.txt
```

## Méthode 1 : Utiliser le script automatique

Exécutez simplement :
```bash
python build_exe.py
```

## Méthode 2 : Commande manuelle

```bash
pyinstaller --name=TikTokLiveMonitor --onefile --windowed --add-data="data;data" --hidden-import=pandas --hidden-import=openpyxl --hidden-import=reportlab --hidden-import=TikTokLive data/gui.py
```

## Résultat

L'exécutable sera créé dans le dossier `dist/TikTokLiveMonitor.exe`

## Distribution

Pour distribuer l'application :
1. Copiez `dist/TikTokLiveMonitor.exe` 
2. Le client n'a besoin d'installer que l'exécutable
3. Le dossier `data` sera inclus dans l'exécutable

## Notes importantes

- La première exécution peut être plus lente (décompression)
- L'antivirus peut parfois signaler un faux positif (normal avec PyInstaller)
- Taille de l'exécutable : ~50-100 MB (toutes les bibliothèques sont incluses)

