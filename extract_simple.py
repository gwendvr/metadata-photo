#!/usr/bin/env python3
"""
Script rapide pour extraire UNIQUEMENT : nom, date/heure, GPS
"""

import sys
import os
from pathlib import Path
from simple_metadata import SimplePhotoMetadata


def main():
    """Fonction principale pour extraction rapide."""
    
    try:
        # Déterminer le dossier à traiter
        if len(sys.argv) > 1:
            photo_dir = sys.argv[1]
        else:
            photo_dir = input("Dossier des photos: ").strip() or "."
        
        if not os.path.exists(photo_dir):
            print(f"Le dossier {photo_dir} n'existe pas.")
            input("Appuyez sur Entree pour continuer...")
            return
        
        print(f"Extraction simple des métadonnées: {photo_dir}")
        print("Récupération de : Nom, Date/Heure, GPS")
        print()
        
        # Créer le gestionnaire
        manager = SimplePhotoMetadata(photo_dir)
        
        # Extraire les métadonnées
        metadata = manager.scan_directory()
        
        if metadata:
            # Sauvegarder
            manager.save_metadata(metadata)
            
            # Afficher le résumé
            manager.display_summary(metadata)
            
            print(f"\nExtraction terminée!")
            print(f"Fichier de sauvegarde: {manager.metadata_file}")
            
        else:
            print("Aucune photo trouvée dans le dossier.")
    
    except Exception as e:
        print(f"\n!!! ERREUR !!!")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Message: {e}")
        import traceback
        traceback.print_exc()
        print("\nAppuyez sur Entree pour continuer...")
        input()


if __name__ == "__main__":
    main()
