import os

def del_vof_srt(st_dir, series):
    for serie in series:
        serie_path = os.path.join(st_dir, serie)
        for root, dirs, files in os.walk(serie_path):
            for file in files:
                if file in ['vo.srt', 'vf.srt']:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted {file_path}")