#!/usr/bin/env python3
"""
Script de test complet pour vérifier le processus d'extraction et de restauration
"""

import os
import sys
from pathlib import Path
from simple_metadata import SimplePhotoMetadata
import json


def find_photos_in_directory(directory):
    """Trouve toutes les photos dans un dossier."""
    photo_dir = Path(directory)
    supported_formats = {'.jpg', '.jpeg', '.tiff', '.tif'}
    photos = []
    
    for file_path in photo_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            photos.append(file_path)
    
    return photos


def test_extraction_restoration():
    """Teste le processus complet d'extraction et de restauration."""
    print("TEST COMPLET D'EXTRACTION ET DE RESTAURATION")
    print("=" * 60)
    
    # Demander le dossier
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = input("Dossier a tester: ").strip() or "."
    
    if not os.path.exists(test_dir):
        print(f"Le dossier {test_dir} n'existe pas.")
        return
    
    # Chercher des photos
    photos = find_photos_in_directory(test_dir)
    print(f"\nPhotos trouvees: {len(photos)}")
    
    if not photos:
        print("Aucune photo trouvee dans le dossier.")
        print("Formats supportes: .jpg, .jpeg, .tiff, .tif")
        return
    
    for photo in photos[:5]:  # Limiter a 5 exemples
        print(f"   {photo.name}")
    
    if len(photos) > 5:
        print(f"   ... et {len(photos) - 5} autres")
    
    # Créer le gestionnaire
    manager = SimplePhotoMetadata(test_dir)
    
    print(f"\nETAPE 1: EXTRACTION DES METADONNEES")
    print("-" * 40)
    
    # Extraire les métadonnées
    metadata = manager.scan_directory()
    
    if not metadata:
        print("Aucune metadonnees extraite.")
        return
    
    print(f"Metadonnees extraites pour {len(metadata)} photos")
    
    # Sauvegarder
    print(f"\nETAPE 2: SAUVEGARDE")
    print("-" * 40)
    manager.save_metadata(metadata)
    print(f"Sauvegarde dans: {manager.metadata_file}")
    
    # Vérifier la sauvegarde
    if manager.metadata_file.exists():
        file_size = manager.metadata_file.stat().st_size
        print(f"Taille du fichier: {file_size} octets")
    
    # Tester le rechargement
    print(f"\nETAPE 3: RECHARGEMENT")
    print("-" * 40)
    reloaded_metadata = manager.load_metadata()
    
    if reloaded_metadata:
        print(f"Recharge de {len(reloaded_metadata)} photos")
        
        # Comparer les données
        print(f"\nETAPE 4: VERIFICATION DES DONNEES")
        print("-" * 40)
        
        for filepath, original_data in metadata.items():
            reloaded_data = reloaded_metadata.get(filepath, {})
            
            print(f"\n{Path(filepath).name}")
            print(f"   Original - Date: {original_data.get('date_creation')}, Heure: {original_data.get('heure_creation')}")
            print(f"   Rechargé - Date: {reloaded_data.get('date_creation')}, Heure: {reloaded_data.get('heure_creation')}")
            
            # Vérifier si les données EXIF sont présentes
            has_original_exif = 'raw_exif' in original_data and original_data['raw_exif']
            has_reloaded_exif = 'raw_exif' in reloaded_data and reloaded_data['raw_exif']
            
            print(f"   EXIF original: {'OK' if has_original_exif else 'NOK'}")
            print(f"   EXIF recharge: {'OK' if has_reloaded_exif else 'NOK'}")
            
            if original_data.get('erreur'):
                print(f"   Erreur extraction: {original_data['erreur']}")
            
            break  # Ne montrer que le premier pour économiser l'espace
        
        # Afficher le résumé
        print(f"\nETAPE 5: RESUME")
        print("-" * 40)
        manager.display_summary(reloaded_metadata)
        
    else:
        print("Erreur lors du rechargement")


if __name__ == "__main__":
    test_extraction_restoration()
