from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import pickle
from flask import session


def process_documents(documents):
    # Création du vectorizer initial avec les paramètres spécifiés
    vectorizer = TfidfVectorizer(stop_words=None, min_df=0.01, max_df=0.95)
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Filtrer pour ne conserver que les mots avec un poids > 0
    non_zero_columns = tfidf_matrix.max(axis=0).toarray().flatten() > 0
    filtered_tfidf_matrix = tfidf_matrix[:, non_zero_columns]
    
    # Extraire les mots correspondants
    filtered_feature_names = np.array(vectorizer.get_feature_names_out())[non_zero_columns]
    
    # Créer un nouveau vectorizer avec le vocabulaire filtré et l'ajuster aux documents
    filtered_vectorizer = TfidfVectorizer(vocabulary=filtered_feature_names)
    filtered_vectorizer.fit(documents)  # Ajuster le nouveau vectorizer
    
    return filtered_tfidf_matrix, filtered_vectorizer



def construct_series(st_dir):
    return {
        serie: [episode for episode in os.listdir(os.path.join(st_dir, serie)) if episode.endswith(".txt")]
        for serie in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, serie))
    }

def load_documents(st_dir, series):
    documents = []
    for serie, episodes in series.items():
        for episode in episodes:
            with open(os.path.join(st_dir, serie, episode), 'r', encoding='latin-1') as file:
                documents.append(file.read())
    return documents

def find_most_similar_series(mot_input, vectorizer, tfidf_matrix, series, documents):
    input_vector = vectorizer.transform([" ".join(mot_input)])
    similarities = cosine_similarity(input_vector, tfidf_matrix)
    if similarities.size == 0:
        return None
    
    top_indices = np.argsort(similarities[0])[::-1][:5]
    top_series = []
    for index in top_indices:
        serie_name = list(series.keys())[index // len(series[list(series.keys())[0]])]
        top_series.append(serie_name)
    return top_series

def main(st_dir, mot_input):
    print("Chargement des sous-titres...")
    series = construct_series(st_dir)
    print("Chargement des documents...")
    documents = load_documents(st_dir, series)
    
    vectorizer_path = 'vectorizer.pkl'
    tfidf_matrix_path = 'tfidf_matrix.pkl'
    
    if os.path.exists(vectorizer_path) and os.path.exists(tfidf_matrix_path):
        print("Fichier trouvé.")
        with open(vectorizer_path, 'rb') as file:
            vectorizer = pickle.load(file)
        with open(tfidf_matrix_path, 'rb') as file:
            tfidf_matrix = pickle.load(file)
    else:
        print("Fichier non trouvé.")
        print("Calcul de la matrice tfidf et du vectorizer...")
        tfidf_matrix, vectorizer = process_documents(documents)
        print("Enregistrement de la matrice tfidf et du vectorizer...")
        with open(tfidf_matrix_path, 'wb') as file:
            pickle.dump(tfidf_matrix, file)
        with open(vectorizer_path, 'wb') as file:
            pickle.dump(vectorizer, file)
    
    print("Recherche de la série la plus similaire...")
    return find_most_similar_series(mot_input, vectorizer, tfidf_matrix, series, documents)




def get_recommandation(st_dir):
    # Récupérer les séries aimées et dislikées depuis la session
    series_like = session.get('liked', [])
    series_dislike = session.get('disliked', [])
    
    # Construire les séries pour recommandation en excluant les likées et dislikées
    series = construct_series_recommandation(st_dir, series_like, series_dislike)
    
    # Chargement des documents
    documents = load_documents(st_dir, series)
    
    print("Calcul de la matrice tfidf...")
    tfidf_matrix, vectorizer = process_documents(documents)
    
    # Initialiser les similarités à zéro
    total_similarities = np.zeros(tfidf_matrix.shape[0])
    
    # Calcul des similarités pour chaque série aimée
    for serie_like in series_like:
        serie_like = str(serie_like)  # Convertir en chaîne de caractères
        input_vector = vectorizer.transform([serie_like])
        similarities = cosine_similarity(input_vector, tfidf_matrix)
        total_similarities += similarities[0]

    # Trier les indices selon les similarités, par ordre décroissant
    sorted_indices = np.argsort(total_similarities)[::-1]
    max_indices = min(len(series), len(sorted_indices))
    
    # Récupérer les recommandations en respectant la limite de séries
    recommandation = []
    for i in sorted_indices[:max_indices]:
        if i < len(series):  # Vérification pour éviter l'IndexError
            recommandation.append(list(series.keys())[i])

    return recommandation[:5]  # Limiter à 5 recommandations maximum


def construct_series_recommandation(st_dir, liked_series, disliked_series):
    # Exclure les séries déjà aimées ou dislikées par l'utilisateur
    return {
        serie: [episode for episode in os.listdir(os.path.join(st_dir, serie)) if episode.endswith(".txt")]
        for serie in os.listdir(st_dir)
        if os.path.isdir(os.path.join(st_dir, serie)) and serie not in liked_series and serie not in disliked_series
    }

# Récupère les séries aimées depuis la session
def getLike():
    return session.get('liked', [])

# Récupère les séries dislikées depuis la session
def getDislike():
    return session.get('disliked', [])








# Exemple d'utilisation
# import time
# start_time = time.time()
# print(get_recommandation("sous-titres"))
# print(f"Temps d'exécution: {time.time() - start_time} secondes.")

# import time
# start_time = time.time()
# st_dir = "sous-titres"
# mot_input = ["leash", "dragon", "ball", "sawyer", "lost"]
# result = main(st_dir, mot_input)
# print("Séries les plus similaires:", result)
# print(f"Temps d'exécution: {time.time() - start_time} secondes.")