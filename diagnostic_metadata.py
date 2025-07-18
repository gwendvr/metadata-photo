#!/usr/bin/env python3
"""
Script de diagnostic pour tester l'extraction des métadonnées
"""

import sys
import os
from pathlib import Path
from simple_metadata import SimplePhotoMetadata
import json


def test_single_photo(photo_path):
    """Teste l'extraction sur une seule photo."""
    print(f"🔍 Test d'extraction sur: {photo_path}")
    
    if not os.path.exists(photo_path):
        print(f"❌ Fichier non trouvé: {photo_path}")
        return
    
    # Créer un gestionnaire temporaire
    photo_dir = Path(photo_path).parent
    manager = SimplePhotoMetadata(photo_dir)
    
    # Extraire les métadonnées de cette photo
    metadata = manager.extract_simple_metadata(Path(photo_path))
    
    print(f"\n📊 RÉSULTATS D'EXTRACTION:")
    print("=" * 50)
    for key, value in metadata.items():
        if key == 'raw_exif':
            print(f"   {key}: [Données EXIF présentes: {len(value) if value else 0} sections]")
        else:
            print(f"   {key}: {value}")
    
    # Tester la sauvegarde et le rechargement
    print(f"\n💾 Test de sauvegarde/rechargement...")
    temp_metadata = {str(photo_path): metadata}
    
    # Sauvegarder
    manager.save_metadata(temp_metadata)
    print(f"✅ Sauvegardé dans: {manager.metadata_file}")
    
    # Recharger
    reloaded = manager.load_metadata()
    if reloaded:
        print(f"✅ Rechargé avec succès")
        reloaded_data = reloaded.get(str(photo_path), {})
        print(f"\n📥 DONNÉES RECHARGÉES:")
        print("-" * 30)
        for key, value in reloaded_data.items():
            if key == 'raw_exif':
                print(f"   {key}: [Données EXIF rechargées: {len(value) if value else 0} sections]")
            else:
                print(f"   {key}: {value}")
    else:
        print(f"❌ Erreur lors du rechargement")


def main():
    """Fonction principale."""
    print("🔧 DIAGNOSTIC D'EXTRACTION DE MÉTADONNÉES")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        photo_path = sys.argv[1]
    else:
        photo_path = input("📁 Chemin vers une photo de test: ").strip()
    
    if not photo_path:
        print("❌ Aucun fichier spécifié.")
        return
    
    test_single_photo(photo_path)


if __name__ == "__main__":
    main()
