import os
import regex as re
import libRecode as libRecode
from ftfy import fix_text

def corriger_texte(texte):
    """Corrige les caractères corrompus dans le texte."""
    return fix_text(texte)

def nettoyer_texte(texte):
    """Nettoie le texte en enlevant les caractères non alphabétiques, sauf les lettres accentuées."""
    texte = re.sub(r'[^a-zA-Z\sÀ-ÿ]', ' ', texte)  # Garder seulement les lettres, les lettres accentuées et les espaces
    return texte

def clean(path):
    # Supprimer les lignes qui commencent par un chiffre
    contenu = re.sub(r'^\d+.*\n?', ' ', path, flags=re.MULTILINE)
    # Supprimer les lignes vides
    contenu = re.sub(r'\n\s*\n', ' ', contenu)
    # Supprimer les retours à la ligne
    contenu = re.sub(r'\n', ' ', contenu)
    # Supprimer les balises HTML
    contenu = re.sub(r'<[^>]*>', ' ', contenu)
    # Supprimer les accolades et leur contenu
    contenu = re.sub(r'\{[^}]*\}', ' ', contenu)
    # Supprimer les parenthèses et leur contenu
    contenu = re.sub(r'\([^)]*\)', ' ', contenu)
    # Supprimer les crochets et leur contenu
    contenu = re.sub(r'\[[^\]]*\]', ' ', contenu)
    # Remplace les | par des espaces
    contenu = re.sub(r'\|', ' ', contenu)
    # Remplace les & par des espaces
    contenu = re.sub(r'&', ' ', contenu)
    # Remplace plusieurs espaces par un seul espace
    contenu = re.sub(r'\s+', ' ', contenu)
    # Remplace ' - ' par un espace
    contenu = re.sub(r' - ', ' ', contenu)
    # Remplace les 'l'' et 'd'' par des espaces
    contenu = re.sub(r"l'", ' ', contenu)
    contenu = re.sub(r"d'", ' ', contenu)
    # Supprime les 'http...' et 'www...'
    contenu = re.sub(r'http\S+', ' ', contenu)
    contenu = re.sub(r'www\S+', ' ', contenu)
    # Supprime les mots de un seul caractère
    contenu = re.sub(r'\b\w\b', ' ', contenu)
    # Supprime les chiffres
    contenu = re.sub(r'\d', ' ', contenu)
    

    contenu = corriger_texte(contenu)
    contenu = nettoyer_texte(contenu)

    # Met tout le contenu en minuscule
    contenu = contenu.lower()
    # Supprime les espaces si il y en a plus d'un
    contenu = re.sub(r'\s+', ' ', contenu)  

    return contenu


def clean_VO_VF(st_dir, series):
    for serie in series:
        for episode in os.listdir(f'{st_dir}/{serie}'):
            if episode.endswith('.txt'):
                with open(f'{st_dir}/{serie}/{episode}', 'r', encoding='latin-1') as file:
                    contenu = file.read()
                contenu = clean(contenu)
                with open(f'{st_dir}/{serie}/{episode}', 'w', encoding='latin-1') as file:
                    file.write(contenu)
                    print(f"Nettoyage du fichier {episode} de la série {serie}")
