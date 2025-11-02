import requests
from bs4 import BeautifulSoup
import json  # Bibliothèque pour travailler avec le format JSON

# URL et Nom du fichier de sortie
URL = "http://books.toscrape.com/"
FICHIER_SORTIE = 'produits_extraits.json'
donnees_produits = [] # Liste pour stocker tous les dictionnaires

print("--- Début de l'Extraction Avancée (JSON) ---")

try:
    reponse = requests.get(URL)
    reponse.raise_for_status()
    soup = BeautifulSoup(reponse.content, 'html.parser')

    # Cibler tous les articles (chaque article représente un livre)
    articles = soup.find_all('article', class_='product_pod')

    for article in articles:
        # 1. Extraction du Titre
        titre = article.h3.a['title']

        # 2. Extraction du Prix (Nécessite de nettoyer le symbole £)
        prix_brut = article.find('p', class_='price_color').text
        prix = prix_brut.replace('£', '').strip()

        # 3. Extraction de la Note (Rating)
        note_brute = article.find('p', class_='star-rating')['class']
        note = note_brute[1] # La note est le deuxième mot de la classe CSS

        # Créer un dictionnaire pour le produit actuel
        produit = {
            'titre': titre,
            'prix': prix,
            'note': note
        }
        donnees_produits.append(produit)

    # Sauvegarder la liste complète en JSON
    with open(FICHIER_SORTIE, 'w', encoding='utf-8') as f:
        json.dump(donnees_produits, f, indent=4) # indent=4 rend le fichier facile à lire

    print(f"\nExtraction réussie de {len(donnees_produits)} produits.")
    print(f"Les données JSON sont enregistrées dans : {FICHIER_SORTIE}")

except requests.exceptions.RequestException as e:
    print(f"Erreur de connexion : {e}")

print("--- Fin de l'Automatisation ---")
