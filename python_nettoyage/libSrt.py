import os
import regex as re

#fonction pour recuperer les fichiers srt par rapport au nom de la serie
def get_srt(st_dir, id_serie):
    # Récupérer les fichiers .srt
    srt_files = [file for file in os.listdir(st_dir + '/' + id_serie) if file.endswith('.srt')]
    return srt_files

#fonction pour recuperer le contenu d'un fichier srt par rapport a son chemin et le nom du fichier
def get_contenu_srt(st_dir, path,fichier_srt):
    # Ouvrir le fichier .srt avec os.listdir
    with open(st_dir + '/' + path + '/' + fichier_srt, 'r',encoding='latin-1') as file:
        contenu = file.read()
    return contenu