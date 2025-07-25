# coding=utf8
import csv
import os
import subprocess

from path.Class import class_folder
from path.docs import docs_folder
from path.error_log import error_log_folder
from path.functions import functions_folder
from path.models import models_folder
from path.odoo import odoo_folder
from path.odoo_backup import odoo_backup_folder, odoo_backup_file
from path.root_path import root_path
from path.sitemaps import sitemaps_folder
from path.res_siren import res_siren_folder, res_siren_file


def init_project():
    """
    Fonction d'initialisation du projet
    Vérification de l'existence des dossiers et fichiers dans le projet :
        - sitemaps/
        - res_siren/
            - res_siren.csv
        - odoo_backup/
            - odoo_backup.csv
    Création des documentations des fichiers de code :
        - Class/
            - Odoo.py
            - ScrapingProcessThread.py
            - ThreadState.py
        - functions/
            - functions_scraping.py
            - init_project.py
            - proxies_list.py
            - soup.py
        - models/
            - odoo_model.py
            - res_siren_model.py
        - odoo/
            - odoo_backup.py
    """
    # Liste des dossiers à créer
    resources_folder = [
        sitemaps_folder,
        res_siren_folder,
        odoo_backup_folder,
        error_log_folder,
    ]
    for path in resources_folder:
        if not os.path.exists(path):
            # Création du dossier s'il n'existe pas
            os.mkdir(path)

    assoc_file = [res_siren_file]
    for assoc in assoc_file:
        if not os.path.exists(assoc):
            # Si le fichier n'existe pas un message s'affiche
            if assoc == res_siren_file:
                print("Importez le fichier res_siren.csv dans :", assoc)
        while not os.path.exists(assoc):
            # En attente de l'ajout du fichier csv s'il n'existe pas
            pass
        print("Fichier existant/ajouté :", assoc)

    file_list = [odoo_backup_file]
    for file in file_list:
        # Initialisation de l'en-tête des fichiers
        with open(file, "w", encoding="utf8", newline="") as csv_scraping:
            writer = csv.writer(csv_scraping)

    # Liste des dossiers contenant du code à documenter avec Pydoc
    code_folder = [
        class_folder,
        functions_folder,
        models_folder,
        odoo_folder,
    ]
    # Suppression des documentations
    docs_files = os.listdir(docs_folder)
    for file in docs_files:
        os.unlink(docs_folder + "/" + file)
    # Déplacement vers le dossier docs/ pour que les documentations soit placées à l'intérieur
    os.chdir(docs_folder)
    os.environ["PYTHONPATH"] = root_path
    for path in code_folder:
        # Pour chaque dossier, on liste les fichiers à documenter
        files = os.listdir(path)
        for file in files:
            if file != "__pycache__" and file.endswith(".py"):
                # Création de la documentation pour chaque fichier
                command = ["python", "-m", "pydoc", "-w", os.path.join(path, file)]
                subprocess.run(command, capture_output=True, text=True)
    # Retour à la racine du projet
    os.chdir(root_path)
