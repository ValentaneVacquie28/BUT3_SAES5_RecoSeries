import os
import zipfile
import time
import chardet
import wordninja

def unzip_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(root)  # Extract to the current root
                        print('Extraction de', file_path)
                    time.sleep(0.1)
                    os.remove(file_path)  # Remove the ZIP file after extraction
                    print('Suppression de', file_path)
                except zipfile.BadZipFile:
                    print(f"Le fichier ZIP est corrompu et ne peut pas être ouvert : {file_path}")
                    try:
                        os.remove(file_path)
                        print(f"Suppression du fichier ZIP corrompu : {file_path}")
                    except Exception as e:
                        print(f"Impossible de supprimer le fichier corrompu : {file_path}. Erreur : {e}")
                except PermissionError as e:
                    print(f"Erreur de permission lors de la suppression de {file_path}: {e}")

def move_files(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            source_path = os.path.join(root, file)
            target_path = os.path.join(directory, file)  # Move to the parent directory
            try:
                os.rename(source_path, target_path)
                print(f"Déplacement de {source_path} vers {target_path}")
            except FileExistsError:
                print(f"Le fichier {target_path} existe déjà dans le dossier {directory}")
            except Exception as e:
                print(f"Erreur lors du déplacement de {source_path} vers {target_path}: {e}")

def delete_unwanted_files(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            if not file.endswith(('.srt', '.SRT', '.txt', '.TXT')):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Suppression de {file_path}")
                except Exception as e:
                    print(f"Erreur lors de la suppression de {file_path}: {e}")

def changeToSrt(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = file_path.rsplit('.', 1)[0] + '.srt'
            try:
                os.rename(file_path, new_file_path)
                print(f"Changement de l'extension de {file_path} en {new_file_path}")
            except Exception as e:
                print(f"Erreur lors du changement de l'extension de {file_path} en .srt: {e}")

# Pas utilisé
def change_encoding(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            # Étape 1 : Détecter l'encodage du fichier
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                print(f"Encodage détecté : {encoding}")

            # Étape 2 : Lire le fichier avec l'encodage détecté et remplacer les erreurs
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()

            # Étape 3 : Enregistrer le texte corrigé dans le même fichier (remplacement)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print("L'encodage a été corrigé et le fichier a été mis à jour.")
    
def delete_empty_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        if not dirs and not files:
            try:
                os.rmdir(root)
                print(f"Suppression du dossier vide: {root}")
            except Exception as e:
                print(f"Erreur lors de la suppression du dossier vide: {root}. Erreur : {e}")

def clean_folder_name(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for folder in dirs:
            new_folder = wordninja.split(folder)
            new_folder = '_'.join(new_folder)
            try:
                os.rename(os.path.join(root, folder), os.path.join(root, new_folder))
                print(f"Renommage du dossier {folder} en {new_folder}")
            except Exception as e:
                print(f"Erreur lors du renommage du dossier {folder} en {new_folder}: {e}")
    clean_folder_name_exception(directory)


# Exceptions pour les noms de dossiers
def clean_folder_name_exception(directory):
    folder_exceptions = {
        'cap_rica': 'caprica',
        'flight_of_the_con_chords': 'flight_of_the_conchords',
        'greys_anatomy': "grey's_anatomy",
        'lie_tome': 'lie_to_me',
        'masters_of_scifi': 'masters_of_science_fiction',
        'swing_town': 'swingtown',
        'the_black_donnelly_s': 'the_black_donnellys',
        'womens_murder_club': "women's_murder_club"
    }
    
    for root, dirs, files in os.walk(directory, topdown=False):
        for folder in dirs:
            if folder in folder_exceptions:
                new_folder = folder_exceptions[folder]
                try:
                    os.rename(os.path.join(root, folder), os.path.join(root, new_folder))
                    print(f"Renommage du dossier {folder} en {new_folder}")
                except Exception as e:
                    print(f"Erreur lors du renommage du dossier {folder} en {new_folder}: {e}")

# Fonction principale de unzip
def unzip(main_directory):
    for dossier in os.listdir(main_directory):
        full_dossier_path = os.path.join(main_directory, dossier)  # Get full path of the subdirectory
        if os.path.isdir(full_dossier_path):  # Ensure it is a directory
            unzip_files(full_dossier_path)  # Unzip files in the subdirectory
            move_files(full_dossier_path)  # Move files from the subdirectory to its parent directory
            delete_unwanted_files(full_dossier_path)    # Delete unwanted files in the subdirectory
            changeToSrt(full_dossier_path)  # Change .txt files to .srt files
            change_encoding(full_dossier_path)  # Change encoding to latin-1
            delete_empty_folders(full_dossier_path) # Delete empty folders in the subdirectory