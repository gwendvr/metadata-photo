# 📸 Extracteur de Métadonnées Photo

Extrait et restaure les métadonnées essentielles des photos : **nom**, **date/heure**, **GPS**.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation rapide

### Extraire les métadonnées
```bash
python extract_simple.py "C:\Chemin\Vers\Photos"
```

### Restaurer les métadonnées
```bash
python restore_simple.py "C:\Dossier\Source" "C:\Dossier\Cible"
```

## Mode interactif
```bash
python simple_metadata.py
```

## Ce qui est extrait

- 📷 **Nom du fichier**
- 📅 **Date et heure** de prise de vue
- 🌍 **Coordonnées GPS** (si disponibles)
- 🔗 **Lien Google Maps** (si GPS disponible)

## Workflow type

1. **Extraire** avant traitement
2. **Traiter** vos photos (retouche, etc.)
3. **Restaurer** les métadonnées sur les photos traitées

Les métadonnées sont sauvées dans `metadata_simple.json` - **gardez ce fichier** pour la restauration !

## Formats supportés

JPEG (.jpg, .jpeg) • TIFF (.tiff, .tif)
