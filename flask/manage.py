from flask import Flask, render_template, request, jsonify, session
from api.api import get_top5_json, get_all_serie_json_by5, get_info_serie
from api.tf_idf import get_recommandation, getLike, getDislike
import os

app = Flask(__name__)
app.secret_key = 'abcdef'  # Nécessaire pour sécuriser la session

# Configurez les cookies de session
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Vous pouvez aussi définir 'Strict' ou 'None' en fonction de vos besoins
app.config['SESSION_COOKIE_SECURE'] = False  # (True quand HTTPS utilisé)

# Chemin des sous-titres
st_dir = "sous-titres"

# Initialiser les listes de séries likées et dislikées dans la session
@app.before_request
def before_request():
    if 'liked' not in session:
        session['liked'] = []
    if 'disliked' not in session:
        session['disliked'] = []

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommandations', methods=['GET'])
def recommandationSeries():
    try:
        # Récupérer les recommandations basées sur les séries likées
        recommandations = get_recommandation(st_dir)
        # Liste vide pour stocker les informations détaillées des séries
        recommandationsInfo = []
        # Récupérer les informations détaillées pour chaque série
        for title in recommandations:
            serie_info = get_info_serie(title)  # Appel de la fonction pour récupérer les détails de la série
            recommandationsInfo.append(serie_info)
        # Passer les séries dislikées et likeées au template
        liked = session.get('liked', [])
        disliked = session.get('disliked', [])
        # Rendre le template HTML avec les informations détaillées et les séries dislikées
        return render_template('recommandation.html', recommandations=recommandationsInfo, disliked=disliked, liked=liked)
    except Exception as e:
        # En cas d'erreur, afficher un message d'erreur et retourner une réponse JSON
        print(f"Erreur lors de la récupération des recommandations : {e}")
        return render_template('recommandation.html', recommandations=[], liked=[], disliked=[])

# Route pour afficher toutes les séries
@app.route('/all_series', methods=['GET'])
def all_series():
    try:
        page = int(request.args.get('page', 1))
        series = get_all_serie_json_by5(st_dir, page)
        
        print(f"Page : {page}")  # Débogage : numéro de page
        print(f"Séries récupérées : {series}")  # Débogage : séries récupérées
        
        liked = session.get('liked', [])
        disliked = session.get('disliked', [])
        
        total_series = len([folder for folder in os.listdir(st_dir) if os.path.isdir(os.path.join(st_dir, folder))])
        total_pages = (total_series // 5) + (1 if total_series % 5 > 0 else 0)
        
        print(f"Total de séries : {total_series}, Pages totales : {total_pages}")  # Débogage
        
        return render_template('allSeries.html', series=series, liked=liked, disliked=disliked, page=page, total_pages=total_pages)
    except Exception as e:
        print(f"Erreur lors de la récupération des séries : {e}")
        return render_template('allSeries.html', series=[], liked=[], disliked=[], page=1, total_pages=1)




#Route pour chercher des series
@app.route('/search', methods=['GET'])
def search_series():
    mots = request.args.get('motSerie')  # Récupération des mots-clés envoyés en paramètre GET
    print(f'Mots reçus : {mots}')  # Affiche les mots reçus
    if mots:
        mots_list = mots.split()  # Transformation en liste de mots
        print(f'Mots sous forme de liste : {mots_list}')  # Affiche la liste de mots
        result = get_top5_json(mots_list)  # Appel de la fonction de recherche
        print(f'Resultat de get_top5_json : {result}')  # Affiche le résultat de la recherche
        return jsonify(result)  # Retour des résultats au format JSON
    else:
        return jsonify({"error": "Aucun mot-clé fourni"})  # Gestion des erreurs


# Route pour récupérer les likes (page allseries)
@app.route('/getLikes', methods=['GET'])
def get_likes():
    try:
        likes = getLike()
        print("Likes récupérés :", likes)  # Debugging
        return jsonify(likes)
    except Exception as e:
        print(f"Erreur lors de la récupération des likes : {e}")
        return jsonify({"error": "Erreur lors de la récupération des likes."})

# Route pour récupérer les dislikes 
@app.route('/getDislikes', methods=['GET'])
def get_dislikes():
    try:
        dislikes = getDislike()
        print("Dislikes récupérés :", dislikes)  # Debugging
        return jsonify(dislikes)
    except Exception as e:
        print(f"Erreur lors de la récupération des dislikes : {e}")
        return jsonify({"error": "Erreur lors de la récupération des dislikes."})

# Route pour gérer les actions like/dislike
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()  # Récupère les données envoyées en JSON
    serie_title = data['id']  # Titre de la série utilisé comme ID
    action = data['action']

    print(f"Titre série : {serie_title}, Action : {action}")  # Afficher le titre et l'action

    # Ajouter ou supprimer le like/dislike dans la session
    if action == 'like':
        if serie_title not in session['liked']:
            session['liked'].append(serie_title)
        if serie_title in session['disliked']:
            session['disliked'].remove(serie_title)
    elif action == 'dislike':
        if serie_title not in session['disliked']:
            session['disliked'].append(serie_title)
        if serie_title in session['liked']:
            session['liked'].remove(serie_title)

    session.modified = True  # Indique que la session a été modifiée

    print("Liked séries:", session.get('liked'))
    print("Disliked séries:", session.get('disliked'))

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)