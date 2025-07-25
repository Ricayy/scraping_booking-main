import threading
import unittest

from functions.functions_scraping import scraping_booking
from models.odoo_model import hotel_data_fields_names


class MyTestCase(unittest.TestCase, threading.Thread):
    def test_scraping_process(self):
        """
        Fonction testant le processus de scraping suivant :
            - Récupération des données (name, adresse, note, ...)
            - Association de l'id Res Partner
            - Ecriture des informations de l'hôtel correspondant à l'id Res Partner

        Examples
        --------
            https://www.booking.com/hotel/fr/du-rocher-lourdes2.fr.html
            https://www.booking.com/hotel/fr/cenntre-rouen.fr.html
            https://www.booking.com/hotel/fr/visane-o.fr.html
            https://www.booking.com/hotel/fr/yuna-porte-maillot-aparthotel.fr.html
            https://www.booking.com/hotel/fr/yuna-saint-germain-serviced-apartments.fr.html
        """

        url_booking = "https://www.booking.com/hotel/fr/alfred-sommier.fr.html"
        result = scraping_booking(url_booking)
        if result is not None:
            nom = result[1][0]
            adr = result[0][hotel_data_fields_names["adresse"]]
            ville = result[0][hotel_data_fields_names["ville"]]
            codePostal = result[0][hotel_data_fields_names["code_postal"]]
            pays = result[0][hotel_data_fields_names["pays"]]
            cat = result[0][hotel_data_fields_names["categorie"]]
            nbEtoile = result[0][hotel_data_fields_names["classement"]]
            nbAvis = result[0][hotel_data_fields_names["nb_avis"]]
            notes = result[0][hotel_data_fields_names["note"]]
            id_siren = result[0][hotel_data_fields_names["id_siren"]]

            print("Nom hôtel :", nom)
            print("Nom de la rue :", adr)
            print("Ville :", ville)
            print("Code postal :", codePostal)
            print("Pays :", pays)
            print("Type d'établissement :", cat)
            print("Nombre d'étoiles Booking :", nbEtoile)
            print("Nombre d'avis :", nbAvis)
            print("Notes :")
            if isinstance(notes, list):
                print("Date scraping :", notes[0][2][hotel_data_fields_names["date_note"]])
                for note in notes:
                    print(f"Note {note[2][hotel_data_fields_names["label_note"]]} :",
                          note[2][hotel_data_fields_names["valeur_note"]])
            else:
                print("Aucune note.")
            print("Correspondance(s) avec l'export Siren :", id_siren)
        else:
            print("lien inexistant")
