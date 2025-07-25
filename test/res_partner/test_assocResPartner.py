import unittest

from Class.Hotel import Hotel
from functions.functions_scraping import assoc_scrap_siren


class TestScrapingScript(unittest.TestCase):

    def test_association_lignes_identiques(self):
        # Données de test
        nomHotel = "Domaine de la Baie de Somme, suite Vanadis"
        adresse = "270 Chemin Guillaume Obry"
        ville = "Cayeux-sur-Mer"
        codePostal = "80410"
        """
        https://www.booking.com/hotel/fr/six-senses-alpine-suites-courchevel.fr.html
        https://www.booking.com/hotel/fr/les-grains-d-argent.fr.html
        https://www.booking.com/hotel/fr/mysuite-bourgoin.fr.html
        https://www.booking.com/hotel/fr/residence-easy-lodge.fr.html
        https://www.booking.com/hotel/fr/kyriad-paris-xv-brancion.fr.html
        https://www.booking.com/hotel/fr/domaine-de-la-baie-de-somme-suite-vanadis.fr.html
        """
        urlHotel = "https://www.booking.com/hotel/fr/citizenm-paris-champs-elysees.fr.html"
        # Appel de la fonction à tester
        resultats = assoc_scrap_siren(adresse, ville, codePostal, urlHotel, Hotel(urlHotel))
        print("id assoc : ", resultats)
        # erreur avec string vide et index out of range

