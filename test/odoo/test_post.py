import unittest

from Class.Hotel import Hotel
from Class.Odoo import Odoo
from Class.ScrapingProcessThread import ScrapingProcessThread
from functions.init_project_folder import init_project
from odoo.odoo_post import create_post_row_odoo


class TestPost(unittest.TestCase):
    def test_post_odoo(self):
        """
        Méthode de publication du fichier odoo_post.csv
        """
        init_project()
        url_hotel = "https://www.booking.com/hotel/fr/alfred-sommier.fr.html"
        # self.test_create_post_row_manually(url_hotel)
        self.test_create_post_row_script(url_hotel)
        # conn = Odoo()
        # conn.split_odoo_post_file()

    def test_create_post_row_manually(self, url_hotel):
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
        class_hotel.set_date_scraping("09/05/2023")
        class_hotel.set_nom_hotel("voco Paris Montparnasse, an IHG Hotel")
        class_hotel.set_adr_complete("79 - 81 avenue du Maine, 14e arr., 75014 Paris, France")
        class_hotel.set_adresse("79 - 81 avenue du Maine 14e arr.")
        class_hotel.set_ville("Paris ")
        class_hotel.set_code_postal("75014")
        class_hotel.set_pays("France")
        class_hotel.set_nombre_etoiles(4)
        class_hotel.set_categorie("Hôtel")
        class_hotel.set_nb_avis("2 804")
        class_hotel.set_note_personnel("8,9")
        class_hotel.set_note_equipements("8,5")
        class_hotel.set_note_proprete("8,9")
        class_hotel.set_note_confort("8,9")
        class_hotel.set_note_qualite_prix("8,2")
        class_hotel.set_note_emplacement("9,0")
        class_hotel.set_note_wifi("8,9")

        create_post_row_odoo(class_hotel)

    def test_create_post_row_script(self, url_hotel):
        """
        Méthode de création d'une ligne de données à publier dans Odoon, en utilisant le processus du script
        Parameters
        ----------
        url_hotel : str
            Url de l'hôtel à publier
        """
        temp = Odoo().query_search_id(url_hotel)
        thread_id = 1
        thread = ScrapingProcessThread(thread_id, url_hotel, temp, "False")
        thread.start()
        thread.join()
