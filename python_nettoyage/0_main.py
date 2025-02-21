import a_unzip as a_unzip
import b_clean as b_clean
import c_combine as c_combine
import d_clean_VO_VF as d_clean_VO_VF
import del_vofSRT as del_vofSRT
import os
import time

st_dir = 'sous-titres'
# series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]

def main():
    start_time = time.time()
    a_unzip.unzip(st_dir)
    del_journeyman(st_dir)
    series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]
    a_unzip.clean_folder_name(st_dir)
    series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]
    b_clean.clean(st_dir, series)
    series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]
    c_combine.combine(st_dir, series)
    series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]
    d_clean_VO_VF.clean_VO_VF(st_dir, series)
    series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]
    del_vofSRT.del_vof_srt(st_dir, series)
    end_time = time.time()
    print("Fin du traitement en", round(end_time - start_time, 2), "secondes")
    
def del_journeyman(st_dir):
    journeyman_path = os.path.join(st_dir, 'journeyman')
    if os.path.exists(journeyman_path):
        try:
            os.remove(journeyman_path)
            print(f"Suppression de {journeyman_path}")
        except Exception as e:
            print(f"Erreur lors de la suppression de {journeyman_path}: {e}")

main()