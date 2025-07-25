# coding=utf8
import os

import requests
from bs4 import BeautifulSoup

from path.root_path import root_path
from path.sitemaps import sitemaps_folder


def download_all_sitemaps():
    """
    Fonction de téléchargement des sitemaps depuis le lien https://www.booking.com/sitembk-hotel-index.xml
    """
    # Récupération et analyse du code source
    page = requests.get("https://www.booking.com/sitembk-hotel-index.xml")
    soup_sitemaps = BeautifulSoup(page.content, "xml")
    # Déplacement vers le dossier sitemaps
    os.chdir(sitemaps_folder)
    # Pour chaque url, on vérifie si le sitemap référence la France
    for url_sitemaps in soup_sitemaps.findAll("loc"):
        if "-fr." in url_sitemaps.text:
            sitemaps_file_name = url_sitemaps.text.split("/")
            open(sitemaps_file_name[len(sitemaps_file_name) - 1], "wb").write(
                requests.get(url_sitemaps.text).content
            )
    # Déplacement vers la racine du projet
    os.chdir(root_path)


def get_sitemaps_list():
    """
    Fonction de récupération de l'ensemble des sitemaps présent dans le dossier

    Returns
    -------
    os.listdir(getSitemapsPath()) : list[str]
    """
    return os.listdir(sitemaps_folder)
