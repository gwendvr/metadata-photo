#!/usr/bin/env python3
"""
Programme simplifié pour extraire uniquement :
- Date de création avec l'heure
- Localisation GPS
- Nom du fichier
"""

import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image
import piexif


class SimplePhotoMetadata:
    """Gestionnaire simplifié des métadonnées des photos."""
    
    def __init__(self, photo_directory):
        """
        Initialise le gestionnaire avec le dossier des photos.
        
        Args:
            photo_directory (str): Chemin vers le dossier contenant les photos
        """
        self.photo_directory = Path(photo_directory)
        self.metadata_file = self.photo_directory / "metadata_simple.json"
        self.supported_formats = {'.jpg', '.jpeg', '.tiff', '.tif', '.heic'}
        
    def get_decimal_from_dms(self, dms, ref):
        """
        Convertit les coordonnées DMS en décimal.
        
        Args:
            dms: Tuple des coordonnées DMS
            ref: Référence (N, S, E, W)
            
        Returns:
            float: Coordonnée en décimal
        """
        if isinstance(dms[0], tuple):
            degrees = dms[0][0] / dms[0][1]
            minutes = dms[1][0] / dms[1][1] / 60.0
            seconds = dms[2][0] / dms[2][1] / 3600.0
        else:
            degrees = dms[0]
            minutes = dms[1] / 60.0
            seconds = dms[2] / 3600.0
        
        result = degrees + minutes + seconds
        
        if ref in ['S', 'W']:
            result = -result
            
        return result
    
    def extract_simple_metadata(self, image_path):
        """
        Extrait uniquement les métadonnées essentielles d'une image.
        
        Args:
            image_path (Path): Chemin vers l'image
            
        Returns:
            dict: Dictionnaire contenant les métadonnées essentielles
        """
        metadata = {
            'nom': image_path.name,
            'date_creation': None,
            'heure_creation': None,
            'gps_latitude': None,
            'gps_longitude': None,
            'localisation': None
        }
        
        try:
            # DATE DE CREATION DU FICHIER SYSTEME (priorite)
            try:
                import platform
                if platform.system() == "Windows":
                    import ctypes
                    from ctypes import wintypes
                    import os
                    kernel32 = ctypes.windll.kernel32
                    handle = kernel32.CreateFileW(
                        str(image_path),
                        0x80000000,  # GENERIC_READ
                        1,           # FILE_SHARE_READ
                        None,        # Default security
                        3,           # OPEN_EXISTING
                        0,           # Normal attributes
                        None         # No template
                    )
                    if handle != -1:
                        class FILETIME(ctypes.Structure):
                            _fields_ = [("dwLowDateTime", wintypes.DWORD),
                                      ("dwHighDateTime", wintypes.DWORD)]
                        creation_time = FILETIME()
                        access_time = FILETIME()
                        write_time = FILETIME()
                        success = kernel32.GetFileTime(
                            handle,
                            ctypes.byref(creation_time),
                            ctypes.byref(access_time),
                            ctypes.byref(write_time)
                        )
                        kernel32.CloseHandle(handle)
                        if success:
                            timestamp_100ns = (creation_time.dwHighDateTime << 32) + creation_time.dwLowDateTime
                            epoch_as_filetime = 116444736000000000
                            timestamp = (timestamp_100ns - epoch_as_filetime) / 10000000.0
                            creation_datetime = datetime.fromtimestamp(timestamp)
                            metadata['date_creation'] = creation_datetime.strftime("%d/%m/%Y")
                            metadata['heure_creation'] = creation_datetime.strftime("%H:%M:%S")
                            print(f"Date creation fichier: {metadata['date_creation']} {metadata['heure_creation']}")
                else:
                    stat_info = image_path.stat()
                    if hasattr(stat_info, 'st_birthtime'):
                        creation_time = stat_info.st_birthtime
                    else:
                        creation_time = stat_info.st_ctime
                    creation_datetime = datetime.fromtimestamp(creation_time)
                    metadata['date_creation'] = creation_datetime.strftime("%d/%m/%Y")
                    metadata['heure_creation'] = creation_datetime.strftime("%H:%M:%S")
            except Exception as e:
                print(f"Erreur lecture date creation fichier pour {image_path.name}: {e}")

            # Extraire les données EXIF (en complément)
            exif_dict = None
            if image_path.suffix.lower() == '.heic':
                # Extraction EXIF pour HEIC
                try:
                    import pyheif
                    import exifread
                    heif_file = pyheif.read(str(image_path))
                    # Les métadonnées EXIF sont dans heif_file.metadata
                    exif_bytes = None
                    for meta in heif_file.metadata:
                        if meta['type'] == 'Exif':
                            exif_bytes = meta['data']
                            break
                    if exif_bytes:
                        import io
                        tags = exifread.process_file(io.BytesIO(exif_bytes), details=False)
                        # On va chercher DateTimeOriginal ou DateTime
                        date_exif = None
                        if 'EXIF DateTimeOriginal' in tags:
                            date_exif = str(tags['EXIF DateTimeOriginal'])
                        elif 'Image DateTime' in tags:
                            date_exif = str(tags['Image DateTime'])
                        if date_exif:
                            try:
                                dt = datetime.strptime(date_exif, "%Y:%m:%d %H:%M:%S")
                                metadata['date_creation'] = dt.strftime("%d/%m/%Y")
                                metadata['heure_creation'] = dt.strftime("%H:%M:%S")
                                print(f"Date EXIF HEIC utilisee: {metadata['date_creation']} {metadata['heure_creation']}")
                            except Exception as e:
                                print(f"Erreur conversion date EXIF HEIC: {e}")
                except Exception as e:
                    print(f"Erreur lecture EXIF HEIC pour {image_path.name}: {e}")
                exif_dict = {}  # Pour ne pas casser la suite
            else:
                exif_dict = piexif.load(str(image_path))
            
            # DATE ET HEURE EXIF (si pas de date fichier systeme)
            if not metadata['date_creation']:
                date_creation = None
                
                # Essayer d'abord DateTimeOriginal (date de prise de vue)
                if "Exif" in exif_dict and piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
                    date_creation = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
                
                # Sinon, essayer DateTime (date de modification)
                elif "0th" in exif_dict and piexif.ImageIFD.DateTime in exif_dict["0th"]:
                    date_creation = exif_dict["0th"][piexif.ImageIFD.DateTime].decode('utf-8')
                
                if date_creation:
                    # Format: "2020:09:12 14:30:25"
                    try:
                        dt = datetime.strptime(date_creation, "%Y:%m:%d %H:%M:%S")
                        metadata['date_creation'] = dt.strftime("%d/%m/%Y")
                        metadata['heure_creation'] = dt.strftime("%H:%M:%S")
                        print(f"Date EXIF utilisee: {metadata['date_creation']} {metadata['heure_creation']}")
                    except:
                        metadata['date_creation'] = date_creation
                        metadata['heure_creation'] = date_creation
            
            # FORCER L'UTILISATION DE LA DATE EXIF DE PRISE DE VUE
            # Cette section remplace la date du système par celle des EXIF si disponible
            date_exif = None
            
            # Essayer d'abord DateTimeOriginal (date de prise de vue)
            if "Exif" in exif_dict and piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
                date_exif = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
            
            # Sinon, essayer DateTime (date de modification)
            elif "0th" in exif_dict and piexif.ImageIFD.DateTime in exif_dict["0th"]:
                date_exif = exif_dict["0th"][piexif.ImageIFD.DateTime].decode('utf-8')
            
            if date_exif:
                # Format: "2020:09:12 14:30:25"
                try:
                    dt = datetime.strptime(date_exif, "%Y:%m:%d %H:%M:%S")
                    metadata['date_creation'] = dt.strftime("%d/%m/%Y")
                    metadata['heure_creation'] = dt.strftime("%H:%M:%S")
                    print(f"Date EXIF de prise de vue utilisee: {metadata['date_creation']} {metadata['heure_creation']}")
                except Exception as e:
                    print(f"Erreur conversion date EXIF: {e}")
            
            # LOCALISATION GPS
            if "GPS" in exif_dict:
                gps_data = exif_dict["GPS"]
                
                # Latitude
                if piexif.GPSIFD.GPSLatitude in gps_data and piexif.GPSIFD.GPSLatitudeRef in gps_data:
                    lat = gps_data[piexif.GPSIFD.GPSLatitude]
                    lat_ref = gps_data[piexif.GPSIFD.GPSLatitudeRef].decode('utf-8')
                    metadata['gps_latitude'] = self.get_decimal_from_dms(lat, lat_ref)
                
                # Longitude  
                if piexif.GPSIFD.GPSLongitude in gps_data and piexif.GPSIFD.GPSLongitudeRef in gps_data:
                    lon = gps_data[piexif.GPSIFD.GPSLongitude]
                    lon_ref = gps_data[piexif.GPSIFD.GPSLongitudeRef].decode('utf-8')
                    metadata['gps_longitude'] = self.get_decimal_from_dms(lon, lon_ref)
                
                # Créer un lien Google Maps si on a les coordonnées
                if metadata['gps_latitude'] and metadata['gps_longitude']:
                    metadata['localisation'] = f"https://www.google.com/maps?q={metadata['gps_latitude']},{metadata['gps_longitude']}"
                
        except Exception as e:
            print(f"Erreur pour {image_path.name}: {e}")
            metadata['erreur'] = str(e)
        
        return metadata
    
    def scan_directory(self):
        """
        Scanne le dossier et extrait les métadonnées essentielles.
        
        Returns:
            dict: Dictionnaire contenant les métadonnées de toutes les photos
        """
        all_metadata = {}
        
        print(f"Scan du dossier: {self.photo_directory}")
        
        for file_path in self.photo_directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                print(f"Traitement de: {file_path.name}")
                metadata = self.extract_simple_metadata(file_path)
                all_metadata[str(file_path)] = metadata
        
        return all_metadata
    
    def save_metadata(self, metadata_dict):
        """
        Sauvegarde les métadonnées dans un fichier JSON.
        
        Args:
            metadata_dict (dict): Dictionnaire des métadonnées
        """
        # Préparer les données pour la sauvegarde
        save_data = {
            'extraction_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'total_photos': len(metadata_dict),
            'photos': {}
        }
        
        for filepath, metadata in metadata_dict.items():
            # Copier les métadonnées sans les données EXIF brutes
            clean_metadata = {k: v for k, v in metadata.items() if k != 'raw_exif'}
            save_data['photos'][filepath] = clean_metadata
            
            # Sauvegarder les données EXIF pour la restauration
            if 'raw_exif' in metadata:
                try:
                    exif_bytes = piexif.dump(metadata['raw_exif'])
                    import base64
                    clean_metadata['raw_exif_b64'] = base64.b64encode(exif_bytes).decode('utf-8')
                except Exception as e:
                    print(f"Erreur sauvegarde EXIF pour {filepath}: {e}")
        
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"Metadonnees sauvegardees: {self.metadata_file}")
    
    def display_summary(self, metadata_dict):
        """
        Affiche un résumé des métadonnées extraites.
        
        Args:
            metadata_dict (dict): Dictionnaire des métadonnées
        """
        print("\n" + "="*60)
        print("RESUME DES METADONNEES EXTRAITES")
        print("="*60)
        
        total_photos = len(metadata_dict)
        photos_avec_gps = 0
        photos_avec_date = 0
        
        print(f"Total des photos: {total_photos}")
        print("\nDETAILS PAR PHOTO:")
        print("-" * 60)
        
        for metadata in metadata_dict.values():
            nom = metadata['nom']
            date = metadata['date_creation'] or "Non trouvee"
            heure = metadata['heure_creation'] or "Non trouvee"
            
            if metadata['gps_latitude'] and metadata['gps_longitude']:
                gps_info = f"GPS: {metadata['gps_latitude']:.4f}, {metadata['gps_longitude']:.4f}"
                photos_avec_gps += 1
            else:
                gps_info = "Pas de GPS"
            
            if metadata['date_creation']:
                photos_avec_date += 1
            
            print(f"{nom}")
            print(f"   Date: {date} a {heure}")
            print(f"   {gps_info}")
            if metadata.get('localisation'):
                print(f"   Carte: {metadata['localisation']}")
            print()
        
        print("-" * 60)
        print(f"STATISTIQUES:")
        print(f"   - Photos avec date: {photos_avec_date}/{total_photos}")
        print(f"   - Photos avec GPS: {photos_avec_gps}/{total_photos}")
        print("=" * 60)
    
    def load_metadata(self):
        """
        Charge les métadonnées depuis le fichier JSON.
        
        Returns:
            dict: Dictionnaire des métadonnées
        """
        if not self.metadata_file.exists():
            print(f"Fichier de metadonnees non trouve: {self.metadata_file}")
            return {}
        
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        metadata_dict = {}
        for filepath, metadata in data.get('photos', {}).items():
            # Reconvertir les données EXIF si nécessaire
            if 'raw_exif_b64' in metadata:
                try:
                    import base64
                    exif_bytes = base64.b64decode(metadata['raw_exif_b64'])
                    metadata['raw_exif'] = piexif.load(exif_bytes)
                    del metadata['raw_exif_b64']
                except Exception as e:
                    print(f"Erreur chargement EXIF pour {filepath}: {e}")
            
            metadata_dict[filepath] = metadata
        
        return metadata_dict
    
    def restore_metadata(self, target_directory=None):
        """
        Restaure les métadonnées sur les photos.
        
        Args:
            target_directory (str): Dossier cible (par défaut: dossier original)
        """
        if target_directory is None:
            target_directory = self.photo_directory
        else:
            target_directory = Path(target_directory)
        
        metadata_dict = self.load_metadata()
        
        if not metadata_dict:
            print("Aucune metadonnees a restaurer.")
            return
        
        print(f"Restauration des metadonnees...")
        
        for original_path, metadata in metadata_dict.items():
            original_filename = Path(original_path).name
            
            # Chercher le fichier dans le dossier cible
            target_files = list(target_directory.rglob(original_filename))
            
            if not target_files:
                print(f"Fichier non trouve: {original_filename}")
                continue
            
            target_file = target_files[0]
            
            try:
                # Charger les EXIF existants du fichier cible
                try:
                    current_exif = piexif.load(str(target_file))
                except:
                    # Si pas d'EXIF, créer une structure vide
                    current_exif = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
                
                # Restaurer la date de création si disponible
                if metadata.get('date_creation') and metadata.get('heure_creation'):
                    try:
                        # Reconvertir la date au format EXIF: "YYYY:MM:DD HH:MM:SS"
                        date_str = metadata['date_creation']  # "16/05/2025"
                        time_str = metadata['heure_creation']  # "17:00:50"
                        
                        # Parser la date
                        day, month, year = date_str.split('/')
                        exif_datetime = f"{year}:{month.zfill(2)}:{day.zfill(2)} {time_str}"
                        
                        print(f"Restauration date: {exif_datetime} pour {target_file.name}")
                        
                        # Mettre à jour les champs de date EXIF
                        current_exif["Exif"][piexif.ExifIFD.DateTimeOriginal] = exif_datetime.encode('utf-8')
                        current_exif["Exif"][piexif.ExifIFD.DateTimeDigitized] = exif_datetime.encode('utf-8')
                        current_exif["0th"][piexif.ImageIFD.DateTime] = exif_datetime.encode('utf-8')
                        
                    except Exception as e:
                        print(f"Erreur conversion date pour {target_file.name}: {e}")
                
                # Restaurer le GPS si disponible
                if metadata.get('gps_latitude') is not None and metadata.get('gps_longitude') is not None:
                    try:
                        lat = float(metadata['gps_latitude'])
                        lon = float(metadata['gps_longitude'])
                        
                        # Convertir en format DMS pour EXIF
                        def decimal_to_dms(decimal):
                            abs_decimal = abs(decimal)
                            degrees = int(abs_decimal)
                            minutes_float = (abs_decimal - degrees) * 60
                            minutes = int(minutes_float)
                            seconds = (minutes_float - minutes) * 60
                            return ((degrees, 1), (minutes, 1), (int(seconds * 1000), 1000))
                        
                        lat_dms = decimal_to_dms(lat)
                        lon_dms = decimal_to_dms(lon)
                        lat_ref = 'N' if lat >= 0 else 'S'
                        lon_ref = 'E' if lon >= 0 else 'W'
                        
                        current_exif["GPS"][piexif.GPSIFD.GPSLatitude] = lat_dms
                        current_exif["GPS"][piexif.GPSIFD.GPSLatitudeRef] = lat_ref.encode('utf-8')
                        current_exif["GPS"][piexif.GPSIFD.GPSLongitude] = lon_dms
                        current_exif["GPS"][piexif.GPSIFD.GPSLongitudeRef] = lon_ref.encode('utf-8')
                        
                        print(f"Restauration GPS: {lat}, {lon} pour {target_file.name}")
                        
                    except Exception as e:
                        print(f"Erreur conversion GPS pour {target_file.name}: {e}")
                
                # Appliquer les metadonnees mises a jour
                exif_bytes = piexif.dump(current_exif)
                piexif.insert(exif_bytes, str(target_file))
                
                # Modifier seulement la date de création du fichier système (pas la modification)
                if metadata.get('date_creation') and metadata.get('heure_creation'):
                    try:
                        from datetime import datetime
                        import time
                        
                        # Reconvertir en objet datetime
                        date_str = metadata['date_creation']  # "16/05/2025"
                        time_str = metadata['heure_creation']  # "17:00:50"
                        
                        day, month, year = date_str.split('/')
                        hour, minute, second = time_str.split(':')
                        
                        # Créer l'objet datetime
                        new_datetime = datetime(
                            int(year), int(month), int(day),
                            int(hour), int(minute), int(second)
                        )
                        
                        # Convertir en timestamp
                        timestamp = new_datetime.timestamp()
                        
                        # Pour Windows : modifier SEULEMENT la date de création (pas la modification)
                        try:
                            import platform
                            if platform.system() == "Windows":
                                import ctypes
                                from ctypes import wintypes
                                
                                # Convertir datetime en FILETIME Windows
                                # FILETIME = nombre de 100-nanosecondes depuis 1er janvier 1601
                                import calendar
                                epoch_as_filetime = 116444736000000000  # January 1, 1970 as FILETIME
                                timestamp_100ns = int(timestamp * 10000000) + epoch_as_filetime
                                
                                # Structures Windows
                                class FILETIME(ctypes.Structure):
                                    _fields_ = [("dwLowDateTime", wintypes.DWORD),
                                              ("dwHighDateTime", wintypes.DWORD)]
                                
                                # Convertir timestamp en FILETIME
                                ft = FILETIME()
                                ft.dwLowDateTime = timestamp_100ns & 0xFFFFFFFF
                                ft.dwHighDateTime = timestamp_100ns >> 32
                                
                                # Ouvrir le fichier avec les bonnes permissions
                                kernel32 = ctypes.windll.kernel32
                                handle = kernel32.CreateFileW(
                                    str(target_file),
                                    0x40000000,  # GENERIC_WRITE
                                    0,           # No sharing
                                    None,        # Default security
                                    3,           # OPEN_EXISTING
                                    0,           # Normal attributes
                                    None         # No template
                                )
                                
                                if handle != -1:  # INVALID_HANDLE_VALUE
                                    # Modifier SEULEMENT la date de création (1er paramètre)
                                    # None, None = ne pas changer accès et modification
                                    success = kernel32.SetFileTime(handle, ctypes.byref(ft), None, None)
                                    kernel32.CloseHandle(handle)
                                    
                                    if success:
                                        print(f"Date creation Windows mise a jour: {new_datetime.strftime('%d/%m/%Y %H:%M:%S')} pour {target_file.name}")
                                        print(f"   (Date de modification preservee)")
                                    else:
                                        print(f"Echec modification date creation Windows pour {target_file.name}")
                                else:
                                    print(f"Impossible d'ouvrir le fichier pour modification date creation: {target_file.name}")
                            else:
                                # Sur autres systèmes, on ne peut modifier que l'accès/modification
                                print(f"Modification date creation non supportee sur {platform.system()}")
                                print(f"   (Seules les dates d'acces/modification peuvent etre modifiees)")
                                
                        except Exception as e:
                            print(f"Erreur modification date creation pour {target_file.name}: {e}")
                        
                    except Exception as e:
                        print(f"Erreur modification date fichier pour {target_file.name}: {e}")
                
                print(f"Restauré: {target_file.name}")
                    
            except Exception as e:
                print(f"Erreur restauration {target_file.name}: {e}")


def main():
    """Fonction principale."""
    print("Extracteur Simple de Metadonnees de Photos")
    print("=" * 45)
    print("Extrait : Nom, Date/Heure, GPS")
    print()
    
    # Demander le dossier des photos
    photo_dir = input("Dossier des photos (ou Entree pour dossier courant): ").strip()
    
    if not photo_dir:
        photo_dir = "."
    
    if not os.path.exists(photo_dir):
        print(f"Le dossier {photo_dir} n'existe pas.")
        return
    
    manager = SimplePhotoMetadata(photo_dir)
    
    while True:
        print("\nOPTIONS:")
        print("1. Extraire les metadonnees")
        print("2. Voir le resume")
        print("3. Restaurer les metadonnees")
        print("4. Quitter")
        
        choice = input("\nChoix (1-4): ").strip()
        
        if choice == "1":
            print("\nExtraction en cours...")
            metadata = manager.scan_directory()
            
            if metadata:
                manager.save_metadata(metadata)
                manager.display_summary(metadata)
            else:
                print("Aucune photo trouvee.")
        
        elif choice == "2":
            metadata = manager.load_metadata()
            if metadata:
                manager.display_summary(metadata)
            else:
                print("Aucune metadonnees sauvegardee.")
        
        elif choice == "3":
            target_dir = input("Dossier cible (ou Entree pour dossier original): ").strip()
            
            if not target_dir:
                target_dir = None
            elif not os.path.exists(target_dir):
                print(f"Le dossier {target_dir} n'existe pas.")
                continue
            
            manager.restore_metadata(target_dir)
        
        elif choice == "4":
            print("\nAu revoir!")
            break
        
        else:
            print("Option invalide.")


if __name__ == "__main__":
    main()
