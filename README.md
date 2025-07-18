# 📸 Extracteur Simple de Métadonnées de Photos

Ce programme extrait et restaure **uniquement** les informations essentielles des photos :
- 📷 **Nom du fichier**
- 📅 **Date et heure de création**
- 🌍 **Localisation GPS**

## 🚀 Installation

1. Assurez-vous d'avoir Python 3.7+ installé
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 📁 Fichiers

- `simple_metadata.py` : Programme principal avec interface interactive
- `extract_simple.py` : Script rapide pour extraire les métadonnées
- `restore_simple.py` : Script rapide pour restaurer les métadonnées
- `extract_simple_120920.bat` : Script Windows pour ton dossier spécifique
- `requirements.txt` : Dépendances Python

## 🔧 Utilisation

### Scripts rapides (recommandé)

#### Extraire les métadonnées
```bash
python extract_simple.py "C:\Mon\Dossier\Photos"
```

#### Restaurer les métadonnées
```bash
python restore_simple.py "C:\Dossier\Source" "C:\Dossier\Cible"
```

#### Pour ton dossier spécifique
Double-cliquez sur `extract_simple_120920.bat`

### Programme interactif
```bash
python simple_metadata.py
```

## � Informations extraites

Le programme extrait **uniquement** :

### 📷 Nom du fichier
- Nom complet du fichier photo

### 📅 Date et heure de création
- Date de prise de vue (format : JJ/MM/AAAA)
- Heure de prise de vue (format : HH:MM:SS)

### 🌍 Localisation GPS
- Latitude et longitude (en décimal)
- Lien Google Maps automatique si GPS disponible

## 💾 Sauvegarde

Les métadonnées sont sauvegardées dans un fichier `metadata_simple.json` qui contient :
- Nom du fichier
- Date et heure de création
- Coordonnées GPS (si disponibles)
- Lien Google Maps (si GPS disponible)
- Données EXIF brutes pour la restauration

## 🔄 Restauration

La restauration permet de :
- Remettre les métadonnées EXIF complètes sur les photos traitées
- Restaurer dans le même dossier ou un dossier différent
- Faire correspondre les photos par nom de fichier

## 🎯 Cas d'usage typiques

1. **Avant traitement** : Extraire les métadonnées
   ```bash
   python extract_simple.py "C:\Users\gwend\Pictures\drive\2020\120920"
   ```

2. **Traiter les photos** (avec votre logiciel préféré)

3. **Après traitement** : Restaurer les métadonnées
   ```bash
   python restore_simple.py "C:\Users\gwend\Pictures\drive\2020\120920" "C:\Photos\Traitées"
   ```

## 📋 Formats supportés

- JPEG (.jpg, .jpeg)
- TIFF (.tiff, .tif)

## ⚠️ Notes importantes

- Les métadonnées EXIF peuvent être perdues lors de l'édition avec certains logiciels
- Toujours faire une sauvegarde avant de modifier les photos
- Le fichier `metadata_backup.json` doit être conservé pour la restauration

## 🐛 Résolution de problèmes

### "Aucune photo trouvée"
- Vérifiez que le dossier contient des fichiers .jpg ou .tiff
- Assurez-vous que le chemin est correct

### "Erreur lors de l'extraction"
- Certains fichiers peuvent avoir des métadonnées corrompues
- Le programme continue avec les autres fichiers

### "Fichier de métadonnées non trouvé"
- Utilisez d'abord l'extraction avant la restauration
- Le fichier `metadata_simple.json` doit être dans le dossier source

## 🔍 Exemple de sortie

```
� Extracteur Simple de Métadonnées de Photos
=============================================
🎯 Extrait : Nom, Date/Heure, GPS

🔍 Scan du dossier: C:\Users\gwend\Pictures\drive\2020\120920
📸 Traitement de: IMG_001.jpg
📸 Traitement de: IMG_002.jpg
📸 Traitement de: IMG_003.jpg

============================================================
📊 RÉSUMÉ DES MÉTADONNÉES EXTRAITES
============================================================
📸 Total des photos: 3

📋 DÉTAILS PAR PHOTO:
------------------------------------------------------------
📷 IMG_001.jpg
   📅 Date: 12/09/2020 à 14:30:25
   ✅ GPS: 48.8584, 2.2945
   🔗 Carte: https://www.google.com/maps?q=48.8584,2.2945

📷 IMG_002.jpg
   📅 Date: 12/09/2020 à 15:45:12
   ❌ Pas de GPS

📷 IMG_003.jpg
   📅 Date: 12/09/2020 à 16:20:08
   ✅ GPS: 48.8566, 2.3522
   🔗 Carte: https://www.google.com/maps?q=48.8566,2.3522

------------------------------------------------------------
📊 STATISTIQUES:
   • Photos avec date: 3/3
   • Photos avec GPS: 2/3
============================================================
```
