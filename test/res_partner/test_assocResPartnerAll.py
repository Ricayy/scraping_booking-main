import unittest
import csv

from functions.functions_scraping import assoc_scrap_siren
from path.root_path import root_path


class TestScrapingScript(unittest.TestCase):

    def test_association_lignes_identiques(self):
        postOdooPath = root_path + "\splitPost\postOdoo.csv"
        csvSrapReader = csv.DictReader(open(postOdooPath, "r", encoding="utf8"))
        count = 0
        type_etablissement = ["Appart'hôtel", "Auberge", "Auberge de jeunesse", "Bateau-hôtel", "Camping",
                              "Complexe hôtelier", "Hôtel", "Lodge", "Love hôtel", "Village vacances"]
        for scrap_row in csvSrapReader:
            idResPartner = ""
            if not scrap_row["x_studio_id_respartner"]:
                for type_unit in type_etablissement:
                    if scrap_row["x_studio_type"] == type_unit:
                        idResPartner = assoc_scrap_siren(scrap_row["x_studio_nom_hotel"],
                                                         scrap_row["x_studio_adresse"],
                                                         scrap_row["x_studio_ville"],
                                                         scrap_row["x_studio_code_postal"],
                                                         scrap_row["x_name"])
                        print("Résultat : ", scrap_row["x_name"])
                        print("Nom :", scrap_row["x_studio_nom_hotel"])
                        print("Adresse : ", scrap_row["x_studio_adresse"])
                        print("Ville : ", scrap_row["x_studio_ville"])
                        print("Code postal : ", scrap_row["x_studio_code_postal"])
                        print("Type : ", scrap_row["x_studio_type"])
                        print("Id assoc : ", idResPartner)
                        print()
                        if idResPartner != "":
                            count = count + 1
                        print(count)
                        break
