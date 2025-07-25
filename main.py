# coding=utf8
"""
Génération docstring : python -m pydoc -w <chemin_complet>
Reformat code : black <chemin_complet>
import pdb; pdb.set_trace()

À faire :
    - Commentaires pour chaque changement
    - Refacto structure de l'exécution des threads (méthode .run())
    - Association Siren avec Booking ou backup Odoo ? (actuellement avec l'adresse de Booking)
    (à tester) - Gestion de multiples associations avec res_siren => s'arreter à la première association (vu avec Stéphane)
    - Gestion limite API/multithreading => écriture data dans csv ? ou tout en flux tendu avec lock+sleep sur thread ?
    - Utilisation du fichier Siren brut (à la place du fichier res_siren) => demandé à Stéphane de faire un extract des
    colonnes qu'il souhaite avoir ou toi-même sur internet en reprenant les champs que l'on utilise sur Odoo
    => réfléchir à API Siren
    - Refonte gestion thread pool et worker ? (ThreadState)
    - Cronjob pour automatiser l'exécution du script selon une échéance (x par mois ?)
"""
import traceback

from Class.Odoo import Odoo
from Class.ScrapingProcessThread import init_thread_list
from Class.ThreadState import start_thread_queue
from functions.date import get_date_log
from functions.init_project import init_project
from functions.sitemaps import download_all_sitemaps
from path.root_path import root_path

if __name__ == "__main__":
    try:
        # Vérification de l'existence des dossiers du projet
        # init_project()
        # Téléchargement de tous les sitemaps depuis les sites de Booking
        # download_all_sitemaps()
        # Authentification Odoo
        conn = Odoo()
        # Backup de la base Odoo avant modification
        # conn.query_odoo_backup()
        # Initialisation de la liste des threads à exécuter (scraping et association res_siren)
        threads = init_thread_list(conn)
        # Exécution de la liste des threads
        start_thread_queue(threads)
    except Exception as e:
        log_file = open(root_path + "/error_log/log.txt", "a")
        # Ecriture de l'erreur dans le fichier log.txt
        log_file.writelines([get_date_log() + " ", "Erreur ", "Traceback "])
        log_file.writelines([str(e), traceback.format_exc()])
        log_file.close()
