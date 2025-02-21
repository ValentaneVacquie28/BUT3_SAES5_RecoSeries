import requests
import os
from dotenv import load_dotenv
import api.tf_idf as tf_idf
import time
#from . import tf_idf #pour tester sur le navigateur

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
st_dir = 'sous-titres'

def get_info_serie(title):
    url = f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}'
    response = requests.get(url)
    response.raise_for_status()  # Ensure we raise an exception for HTTP errors
    return response.json()

def get_top5_json(mots):
    top5 = tf_idf.main(st_dir, mots)
    if not top5:
        return {"error": "Aucune série trouvée"}
    
    top5_json = []
    for serie in top5:
        try:
            serie_info = get_info_serie(serie)
            if not serie_info:
                print(f"No data found for {serie}")
                continue
            top5_json.append(serie_info)
        except requests.RequestException as e:
            print(f"Error fetching data for {serie}: {e}")
            continue
    return top5_json

def get_top5(mots):
    top5 = tf_idf.main(st_dir, mots)
    return top5

def get_serie_problem_name(dir):
    series = [folder for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]
    for serie in series:
        serie_info = get_info_serie(serie)
        if not 'Title' in serie_info:
            print(serie)

def get_all_serie_json_by5(st_dir, page):
    series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]
    series_json = []
    for i in range((page - 1) * 5, min(page * 5, len(series))):
        serie = series[i]
        try:
            serie_info = get_info_serie(serie)
            if not serie_info:
                print(f"No data found for {serie}")
                continue
            series_json.append(serie_info)
        except requests.RequestException as e:
            print(f"Error fetching data for {serie}: {e}")
            continue
    return series_json

def get_all_serie_json(st_dir):
    series = [folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))]
    series_json = []
    for serie in series:
        try:
            serie_info = get_info_serie(serie)
            if not serie_info:
                print(f"No data found for {serie}")
                continue
            series_json.append(serie_info)
        except requests.RequestException as e:
            print(f"Error fetching data for {serie}: {e}")
            continue
    return series_json



# mots = ['leash', 'dragon', 'ball', 'sawyer', 'lost']
# start_time = time.time()
# # print(get_top5_json(mots))
# print(get_top5(mots))
# # get_serie_problem_name(st_dir)
# # print(get_all_serie_json_by5(st_dir, 2))
# end_time = time.time()
# print("Fin du traitement en", round(end_time - start_time, 2), "secondes")
