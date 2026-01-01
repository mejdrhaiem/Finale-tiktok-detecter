# Guide pour créer un exécutable Windows

Ce guide explique comment créer un fichier exécutable (.exe) de votre application TikTok Live Monitor pour la distribuer à vos clients.

## 🎯 Objectif

Créer un fichier `.exe` que vos clients peuvent exécuter directement sans installer Python.

## 📋 Prérequis

1. **Python 3.8+** installé sur votre machine
2. **Toutes les dépendances** installées
3. **PyInstaller** installé

## 🚀 Étapes rapides

### 1. Installer PyInstaller

```bash
pip install pyinstaller
```

### 2. Créer l'exécutable

**Option A : Utiliser le script automatique (recommandé)**

```bash
python build_exe.py
```

**Option B : Utiliser le fichier .spec**

```bash
pyinstaller build.spec
```

**Option C : Commande manuelle**

```bash
pyinstaller --name=TikTokLiveMonitor --onefile --windowed --hidden-import=pandas --hidden-import=openpyxl --hidden-import=reportlab --hidden-import=TikTokLive data/gui.py
```

### 3. Trouver l'exécutable

L'exécutable sera créé dans le dossier `dist/` :
- `dist/TikTokLiveMonitor.exe`

## 📦 Distribution

### Pour vendre à vos clients :

1. **Copiez l'exécutable** `TikTokLiveMonitor.exe`
2. **Créez un package** avec :
   - `TikTokLiveMonitor.exe`
   - Un fichier README.txt avec les instructions d'utilisation
   - (Optionnel) Un fichier de licence

3. **Distribution** :
   - Par email (si fichier < 100MB)
   - Google Drive / Dropbox
   - USB / Disque
   - Site web de téléchargement

## ⚠️ Notes importantes

### Taille de l'exécutable
- Taille attendue : **50-100 MB**
- Toutes les bibliothèques Python sont incluses dans l'exécutable
- Le client n'a besoin d'installer RIEN d'autre

### Antivirus
- Les exécutables PyInstaller peuvent être signalés par certains antivirus (faux positif)
- C'est normal et courant avec PyInstaller
- Solutions :
  - Ajoutez une signature de code (payant)
  - Utilisez un certificat de développeur
  - Informez vos clients que c'est un faux positif

### Compatibilité
- L'exécutable fonctionne uniquement sur **Windows**
- Testez sur une machine Windows propre avant distribution
- Pour Mac/Linux, créez des exécutables séparés

## 🔧 Personnalisation

### Ajouter une icône

1. Créez ou téléchargez un fichier `.ico`
2. Ajoutez `--icon=chemin/vers/icone.ico` dans les options

### Changer le nom

Modifiez `--name=VotreNomApp` dans `build_exe.py`

### Version avec console (pour débogage)

Remplacez `--windowed` par `--console` pour voir les erreurs

## 📝 Checklist avant distribution

- [ ] Tester l'exécutable sur une machine Windows propre
- [ ] Vérifier que toutes les fonctionnalités marchent
- [ ] Créer un README pour le client
- [ ] Préparer les instructions d'installation
- [ ] Tester le téléchargement du PDF
- [ ] Vérifier la détection des numéros
- [ ] Préparer un fichier de licence si nécessaire

## 💡 Conseils pour la vente

1. **Version d'essai** : Créez une version avec limitations (ex: max 10 numéros)
2. **Licence** : Implémentez un système de clé de licence
3. **Support** : Préparez un email/chat pour le support client
4. **Documentation** : Créez un guide utilisateur simple
5. **Mise à jour** : Prévoyez un système de mise à jour si nécessaire

## 🆘 Problèmes courants

**Erreur "ModuleNotFoundError"**
- Ajoutez `--hidden-import=nom_module` dans les options

**Exécutable trop volumineux**
- Utilisez `--exclude-module` pour exclure des modules inutiles

**L'exécutable ne démarre pas**
- Utilisez `--console` au lieu de `--windowed` pour voir les erreurs
- Vérifiez les logs dans le dossier temporaire

**Fichiers manquants**
- Vérifiez que tous les fichiers nécessaires sont inclus avec `--add-data`

## 📞 Support

Si vous rencontrez des problèmes, vérifiez :
1. La documentation PyInstaller : https://pyinstaller.org/
2. Les logs dans le dossier `build/`
3. Les messages d'erreur avec `--console`

