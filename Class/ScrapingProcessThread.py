# coding=utf8
import csv
import gzip
import os
import threading
import time
import traceback

from bs4 import BeautifulSoup

from Class.Odoo import Odoo
from functions.date import get_date_log
from functions.functions_scraping import (
    assoc_scrap_odoo_backup,
    assoc_scrap_siren,
    scraping_booking,
)
from models.odoo_model import OdooContactModel
from path.root_path import root_path
from path.sitemaps import sitemaps_folder


def init_thread_list(conn):
    """
    Initialisation de la liste de threads selon les sitemaps

    Returns
    -------
    threads : list[ScrapingProcessThread]
        Liste des threads à executer
    """
    # # Récupération de la liste des sitemaps
    # sitemaps_list_dir = os.listdir(sitemaps_folder)
    # sitemaps_set = set()
    # # Lecture des sitemaps
    # for sitemaps_name in sitemaps_list_dir:
    #     soup = BeautifulSoup(gzip.open(sitemaps_folder + "/" + sitemaps_name, "rb").read(), "xml")
    #     # Lecture des url dans les sitemaps
    #     for url_hotel in soup.findAll("loc"):
    #         url_hotel = url_hotel.text
    #         # Si un hôtel se trouve en France alors, on l'ajoute à l'ensemble destiné au scraping
    #         if "https://www.booking.com/hotel/fr/" in url_hotel:
    #             sitemaps_set.add(url_hotel)
    # print("len(sitemaps_set)", len(sitemaps_set))
    sitemaps_set = [
        "https://www.booking.com/hotel/fr/alfred-sommier.fr.html",
        # "https://www.booking.com/hotel/fr/scribe-paris.fr.html"
    ]
    thread_id = 1
    threads_list = []
    for url_hotel in sitemaps_set:
        # Initialisation d'un thread pour chaque lien présent dans les sitemaps
        threads_list.append(ScrapingProcessThread(conn, thread_id, url_hotel))
        thread_id += 1
    print("Nombre de thread initalisés :", thread_id - 1)

    return threads_list


class ScrapingProcessThread(threading.Thread):
    """
    Classe ScrapingProcessThread contenant :
        - L'initialisation des threads (id, name et url_hotel)
        - La vérification de l'éxistence de l'url Booking dans le backup d'Odoo
        - Le scraping de la page Booking et écriture des résultats dans le fichier CSV de publication
        - Méthode get pour la récupération de l'id et name du thread

    Attributes
    ----------
    thread_name : str
        Nom du thread
    thread_id : int
        Identifiant du thread
    url_hotel : str
        Url de l'établissement
    hotel_data : list[]
        Liste des données de l'établissement
    thread_lock : threading.Lock
        Verrou des threads, un thread à la fois peut accéder au code encapsuler (lock->acquire)

    Methods
    -------
    __init__ (self, thread_id, url_hotel) :
        Constructeur de la classe ScrapingProcessThread initialisant les variables nécessaires pour l'exécution du thread
    run (self) :
        Méthode d'exécution du thread
    """

    thread_name = ""
    thread_id = ""
    url_hotel = ""
    hotel_data = []
    thread_lock = threading.Lock()

    def __init__(self, conn, thread_id, url_hotel):
        """
        Constructeur de la classe ScrapingProcessThread initialisant les variables pour l'exécution du thread

        Parameters
        ----------
        conn : Odoo
            Objet Odoo
        thread_id : int
            Identifiant du thread
        url_hotel : str
            Url Booking associé au thread
        """
        threading.Thread.__init__(self)
        self.conn = conn
        self.thread_id = thread_id
        self.thread_name = f"Thread {thread_id}"
        self.url_hotel = url_hotel

    def run(self):
        """
        Méthode d'exécution du thread :

        Pour chaque url Booking un thread est démarré et le traitement suivant est effectué :
            - Scraping de la page Booking et association à respartner et siren
            - Si le lien n'existe pas dans Odoo alors, on effectue la publication sinon, on effectue la modification
        """
        try:
            print("Starting", self.thread_name)
            # Scraping de la page Booking
            self.hotel_data = scraping_booking(self.url_hotel)
            print("scrap done")
            if self.hotel_data != {}:
                """
                Nouvelle logique ?
                Query url hotel sur Odoo -> lock
                Si url trouvé dans Odoo:
                    Récupération id Odoo
                    Depuis query url hotel on peut récupérer id_siren
                    Si id_siren existant:
                        Pas de modification des données Siren
                    Sinon (n'existe pas):
                        Recherche de l'adresse Booking dans Siren
                    Modification de la ligne Odoo en utilisant l'id
                Sinon (false reçu si n'existe pas ?):
                    Recherche adresse Booking dans le backup Odoo
                    Recherche adresse Booking dans Siren
                    Si adresse existe dans Odoo:
                        Récupération de l'id Odoo et infos Siren
                        Modification de l'établissement les infos Booking et Siren
                    Sinon (n'existe pas):
                        Récupération de l'id Odoo et infos Siren
                        Création d'un nouvel établissement avec les infos Booking et Siren
                """
                res_name = assoc_scrap_siren(self.hotel_data)
                # Récupération de l'id Odoo en comparant l'url Booking ou l'adresse avec les enregistrements d'Odoo
                id_odoo = assoc_scrap_odoo_backup(self.hotel_data)
                self.thread_lock.acquire()
                if id_odoo:
                    # Si l'établissement existe
                    print(res_name, "existe")
                    self.hotel_data.pop(OdooContactModel().name, None)
                    # Publication de la modification sur Odoo
                    self.conn.query_odoo_put(id_odoo, self.hotel_data[0])
                    time.sleep(0.5)
                else:
                    print("nouveau", self.thread_name, self.url_hotel)
                    # Si l'établissement n'existe pas
                    self.conn.query_odoo_post(self.hotel_data[0])
                    time.sleep(0.5)
                self.thread_lock.release()
            print("Exiting", self.thread_name)
        except Exception as e:
            log_file = open(root_path + "/error_log/log.txt", "a")
            # Ecriture de l'erreur dans le fichier log.txt
            log_file.writelines(
                [get_date_log() + " ", self.thread_name + " ", "Erreur ", "Traceback "]
            )
            log_file.writelines([self.url_hotel, str(e), traceback.format_exc()])
            log_file.close()
