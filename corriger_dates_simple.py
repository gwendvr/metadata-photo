#!/usr/bin/env python3
"""
Programme simple pour corriger les dates et heures de création dans un fichier 
de métadonnées photos en se basant sur les noms de fichiers.
"""

import json
import re
from datetime import datetime

def extract_date_from_filename(filename):
    """
    Extrait la date et l'heure du nom de fichier.
    
    Args:
        filename (str): Nom de fichier à analyser
        
    Returns:
        tuple: (date_creation, heure_creation) ou (None, None) si non trouvé
    """
    # Format avec date et heure: 20210711_065821.jpg
    match = re.search(r'(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})', filename)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        hour = match.group(4)
        minute = match.group(5)
        second = match.group(6)
        
        date_fr = f"{day}/{month}/{year}"
        heure = f"{hour}:{minute}:{second}"
        return date_fr, heure
        
    # Format WhatsApp: 20210711-WA0000.jpg
    match = re.search(r'(\d{4})(\d{2})(\d{2})-WA', filename)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        
        date_fr = f"{day}/{month}/{year}"
        # On ne change pas l'heure existante
        return date_fr, None
    
    return None, None

def correct_metadata_dates(input_file, output_file):
    """
    Corrige les dates et heures dans le fichier de métadonnées.
    
    Args:
        input_file (str): Fichier d'entrée (JSON)
        output_file (str): Fichier de sortie (JSON)
    """
    print(f"Lecture du fichier {input_file}...")
    
    # Charger les métadonnées
    with open(input_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print(f"Total de photos trouvées: {metadata.get('total_photos', 0)}")
    
    # Date future incorrecte à corriger
    date_future = "21/05/2025"
    corrections = 0
    
    # Parcourir toutes les photos
    for filepath, photo_data in metadata['photos'].items():
        filename = photo_data['nom']
        
        # Vérifier si la date est incorrecte (année 2025)
        if photo_data['date_creation'] and date_future in photo_data['date_creation']:
            date_from_name, heure_from_name = extract_date_from_filename(filename)
            
            if date_from_name:
                # Mise à jour de la date de création
                photo_data['date_creation'] = date_from_name
                
                # Mise à jour de l'heure si disponible
                if heure_from_name:
                    photo_data['heure_creation'] = heure_from_name
                
                corrections += 1
                print(f"Correction de {filename} -> {date_from_name} {heure_from_name or photo_data['heure_creation']}")
    
    # Mettre à jour la date d'extraction
    metadata['extraction_date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Sauvegarder les métadonnées corrigées
    print(f"\nSauvegarde des métadonnées corrigées dans {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\nTerminé! {corrections} dates corrigées.")

# Programme principal
if __name__ == "__main__":
    input_file = "metadata_simple.json"
    output_file = "metadata_simple_corrected.json"
    
    print("=== Correction des dates et heures des photos ===")
    correct_metadata_dates(input_file, output_file)