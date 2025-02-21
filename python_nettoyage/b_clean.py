import os
import regex as re
import libSrt as lib

def supprimer_lignes_vides(st_dir, path, fichier_srt):
    contenu = lib.get_contenu_srt(st_dir, path, fichier_srt)
    # Supprimer les lignes qui commencent par un chiffre
    contenu = re.sub(r'^\d+.*\n?', ' ', contenu, flags=re.MULTILINE)
    # Supprimer les lignes vides
    contenu = re.sub(r'\n\s*\n', ' ', contenu)
    #enregistrer le fichier
    with open(st_dir + '/' + path + '/' + fichier_srt, 'w', encoding='latin-1') as file:
        file.write(contenu)

def supprimer_retour_ligne(st_dir, path, fichier_srt):
    contenu = lib.get_contenu_srt(st_dir, path, fichier_srt)
    # Supprimer les retours à la ligne
    contenu = re.sub(r'\n', ' ', contenu)
    #enregistrer le fichier
    with open(st_dir + '/' + path + '/' + fichier_srt, 'w', encoding='latin-1') as file:
        file.write(contenu)

def supprimer_balisage(st_dir, path, fichier_srt):
    contenu = lib.get_contenu_srt(st_dir, path, fichier_srt)
    # Supprimer les balises HTML
    contenu = re.sub(r'<[^>]*>', ' ', contenu)
    #enregistrer le fichier
    with open(st_dir + '/' + path + '/' + fichier_srt, 'w', encoding='latin-1') as file:
        file.write(contenu)

def clean(st_dir, series):
    for serie in series:
        print(f"Nettoyage de la série {serie}")
        if not os.listdir(os.path.join(st_dir, serie)):
            os.rmdir(os.path.join(st_dir, serie))
            continue
        for episode in lib.get_srt(st_dir, serie):
            supprimer_lignes_vides(st_dir, serie, episode)
            supprimer_retour_ligne(st_dir, serie, episode)
            supprimer_balisage(st_dir, serie, episode)
            print(f"Nettoyage de {episode} terminé")