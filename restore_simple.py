#!/usr/bin/env python3
"""
Script rapide pour restaurer les métadonnées simplifiées
"""

import sys
import os
from pathlib import Path
from simple_metadata import SimplePhotoMetadata


def main():
    """Fonction principale pour restauration rapide."""
    
    # Déterminer les dossiers
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    else:
        source_dir = input("Dossier source (avec metadata_simple.json): ").strip() or "."
    
    if not os.path.exists(source_dir):
        print(f"Le dossier source {source_dir} n'existe pas.")
        return
    
    if len(sys.argv) > 2:
        target_dir = sys.argv[2]
    else:
        target_dir = input("Dossier cible (ou Entrée pour dossier source): ").strip()
        if not target_dir:
            target_dir = None
    
    if target_dir and not os.path.exists(target_dir):
        print(f"Le dossier cible {target_dir} n'existe pas.")
        return
    
    print(f"Restauration des métadonnees...")
    print(f"Source: {source_dir}")
    print(f"Cible: {target_dir if target_dir else source_dir}")
    
    # Créer le gestionnaire
    manager = SimplePhotoMetadata(source_dir)
    
    # Vérifier si le fichier de métadonnées existe
    if not manager.metadata_file.exists():
        print(f"Fichier de metadonnees non trouve: {manager.metadata_file}")
        print("Utilisez d'abord extract_simple.py pour extraire les metadonnees.")
        return
    
    # Charger et afficher les métadonnées extraites
    print(f"\nLecture des metadonnees depuis: {manager.metadata_file}")
    
    # Essayons de lire le fichier JSON brut d'abord
    try:
        import json
        with open(manager.metadata_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        print(f"\nINFORMATIONS DU FICHIER:")
        print("=" * 50)
        print(f"Date d'extraction: {raw_data.get('extraction_date', 'Non specifiee')}")
        print(f"Nombre total de photos: {raw_data.get('total_photos', 0)}")
        
        # Afficher quelques échantillons de données
        photos = raw_data.get('photos', {})
        if photos:
            print(f"\nECHANTILLON DES DONNEES EXTRAITES:")
            print("-" * 50)
            for i, (filepath, metadata) in enumerate(photos.items()):
                if i >= 3:  # Limiter à 3 exemples
                    break
                print(f"{Path(filepath).name}")
                print(f"   Date extraite: {metadata.get('date_creation', 'Non trouvée')}")
                print(f"   Heure extraite: {metadata.get('heure_creation', 'Non trouvée')}")
                print(f"   GPS: Lat={metadata.get('gps_latitude', 'N/A')}, Lon={metadata.get('gps_longitude', 'N/A')}")
                print(f"   Chemin: {filepath}")
                if metadata.get('erreur'):
                    print(f"   Erreur: {metadata['erreur']}")
                print()
        
    except Exception as e:
        print(f"Erreur lecture fichier JSON: {e}")
        return
    
    # Maintenant charger via le gestionnaire
    metadata_dict = manager.load_metadata()
    
    if not metadata_dict:
        print("Aucune metadonnees trouvees dans le fichier via le gestionnaire.")
        return
    
    # Afficher les métadonnées qui ont été extraites
    print(f"\nRESUME DES METADONNEES:")
    manager.display_summary(metadata_dict)
    
    # Demander confirmation avant restauration
    print(f"\nVoulez-vous restaurer ces metadonnees sur les photos ?")
    confirmation = input("Tapez 'oui' pour continuer: ").strip().lower()
    
    if confirmation in ['oui', 'o', 'yes', 'y']:
        print(f"\nRestauration en cours...")
        # Restaurer les métadonnées
        manager.restore_metadata(target_dir)
        print("\nRestauration terminee!")
    else:
        print("\nRestauration annulee.")


if __name__ == "__main__":
    main()
