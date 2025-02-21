import os
import regex as re
import libSrt as lib

def combine_VO(st_dir, series):
    for serie in series:
        vo_file_path = f'{st_dir}/{serie}/vo.txt'
        if os.path.exists(vo_file_path):
            os.remove(vo_file_path)
        with open(f'{st_dir}/{serie}/vo.txt', 'a', encoding='utf-8') as vo_file:
            for episode in lib.get_srt(st_dir, serie):
                if 'VO' not in episode and 'english' not in episode and 'EN' not in episode:
                    continue
                contenu = lib.get_contenu_srt(st_dir, serie, episode)
                vo_file.write(contenu)
                vo_file.write('\n\n')
                print(f"Combinaison des fichiers VO de la série {serie}, épisode {episode}")
                os.remove(f'{st_dir}/{serie}/{episode}')

def combine_VF(st_dir, series):
    for serie in series:
        vo_file_path = f'{st_dir}/{serie}/vf.txt'
        if os.path.exists(vo_file_path):
            os.remove(vo_file_path)
        with open(f'{st_dir}/{serie}/vf.txt', 'a', encoding='utf-8') as vo_file:
            for episode in lib.get_srt(st_dir, serie):
                if 'VO' in episode or 'english' in episode or 'EN' in episode:
                    continue
                contenu = lib.get_contenu_srt(st_dir, serie, episode)
                vo_file.write(contenu)
                vo_file.write('\n\n')
                print(f"Combinaison des fichiers VF de la série {serie}, épisode {episode}")
                os.remove(f'{st_dir}/{serie}/{episode}')

def combineChuck(st_dir):
    vf_file_path = f'{st_dir}/chuck/chucks02e10VF.txt'
    if os.path.exists(vf_file_path):
        with open(vf_file_path, 'r', encoding='utf-8') as vf_file:
            contenu = vf_file.read()
        with open(f'{st_dir}/chuck/vf.txt', 'a', encoding='utf-8') as vf_combined_file:
            vf_combined_file.write(contenu)
            vf_combined_file.write('\n\n')
        os.remove(vf_file_path)

def combine(st_dir, series):
    combine_VO(st_dir, series)
    combine_VF(st_dir, series)
    combineChuck(st_dir)
