# scraping_booking
 
Génération docstring : python -m pydoc -w <chemin_complet>

# Prérequis après clonage du projet :
- pip install -r requirements.txt
- ajout du fichier res_siren.csv dans le dossier res_siren/
- création du .env, contenant les informations de connexion au service Odoo (selon le fichier .env.example)
- python main.py

# Processus du scraping sur le site Booking :
- Vérification de l'existence des dossiers de l'architecture
- Téléchargement des sitemaps Booking contenant les liens des hôtels sur Booking (scraping effectué sur la totalité des hôtels français)
- Scraping en multithreading du nom, adresse, code postal, ville, pays, type d'établissement, nombre d'avis, notes et url page Booking
- Création d'une relation entre les hotels Booking et les bases de données Res Partner et Siren (res_siren.csv) à l'aide d'une colonne id et d'une colonne détail (id : numéro de voie, nom de voie + compléments, ville, code postal)
- Utilisation d'une colonne id_status pour déterminer si l'association est correct pour qu'elle ne soit plus modifié (mettre à jour à la main)
- Authentification à l'API Odoo Online
- Publication d'un CSV contenant toutes les nouvelles informations
- Publication d'un CSV contenant toutes les modifications à apporter
