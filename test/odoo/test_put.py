import csv
import time
import unittest

from Class.Hotel import Hotel
from Class.Odoo import Odoo
from Class.ScrapingProcessThread import ScrapingProcessThread
from functions.init_project_folder import init_project
from odoo.odoo_put import create_put_row_odoo


class TestPut(unittest.TestCase):
    def test_execute_surey_put(self):
        Odoo().query_odoo_put()
    def test_query_put(self):
        """
        Méthode de publication des lignes de données à modifié
        """
        init_project()
        url_hotel = "https://www.booking.com/hotel/fr/serenite-marine-maison-en-bord-de-mer-a-notre-dame-de-monts.fr.html"
        id_odoo = Odoo().query_search_id(url_hotel)
        # self.test_put_row_manually(id_odoo, url_hotel)
        self.test_put_row_script(id_odoo, url_hotel)
        Odoo().query_odoo_put()

    def test_put_row_manually(self, id_odoo,  url_hotel):
        """
        Méthode de création d'une nouvelle ligne de données à publier dans Odoo

        Parameters
        ----------
        url_hotel : str
            Url de l'hôtel à publier
        """
        class_hotel = Hotel(url_hotel)
        class_hotel.set_id_res("")
        class_hotel.set_detail_id_res("")
        class_hotel.set_id_siren("")
        class_hotel.set_detail_id_siren("")
        class_hotel.set_date_scraping("")
        class_hotel.set_nom_hotel("")
        class_hotel.set_adr_complete("")
        class_hotel.set_adresse("")
        class_hotel.set_ville("")
        class_hotel.set_code_postal("")
        class_hotel.set_pays("")
        class_hotel.set_nombre_etoiles(0)
        class_hotel.set_categorie("")
        class_hotel.set_nb_avis("")
        class_hotel.set_note_personnel("")
        class_hotel.set_note_equipements("")
        class_hotel.set_note_proprete("")
        class_hotel.set_note_confort("")
        class_hotel.set_note_qualite_prix("")
        class_hotel.set_note_emplacement("")
        class_hotel.set_note_wifi("")
        id_backup = id_odoo

        create_put_row_odoo(class_hotel, id_backup)

    def test_put_row_script(self, id_odoo, url_hotel):
        """
        Méthode de création de la ligne de données à modifier sur Odoo

        Parameters
        ----------
        id_odoo : str
            Identifiant de la ligne Odoo
        url_hotel : str
            Url de l'hôtel à modifier
        """
        thread_id = 1
        thread = ScrapingProcessThread(thread_id, url_hotel, id_odoo, "False")
        thread.start()
        thread.join()
