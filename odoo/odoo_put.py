# coding=utf8
import csv

from path.root_path import root_path

# Chemin vers le dossier et fichier odoo_put
odoo_put_folder = root_path + "/odoo_put"
odoo_put_file = odoo_put_folder + "/odoo_put.csv"


def create_put_row_odoo(init_hotel, id_backup):
    """
    Fonction d'écriture des modifications dans odoo_put.csv

    Parameters
    ----------
    id_backup : str
        Id de la ligne attribuée par Odoo
    init_hotel : Hotel
        Instance de la classe Hotel
    """
    # Ecriture d'une ligne de donnée dans le CSV de modification
    with open(odoo_put_file, "a", encoding="utf8", newline="") as csvResult:
        fieldnames_odoo = get_fieldnames_odoo()
        writer = csv.DictWriter(csvResult, fieldnames=fieldnames_odoo)
        writer.writerow(
            {
                fieldnames_odoo[0]: id_backup,
                fieldnames_odoo[1]: init_hotel.get_id_res(),
                fieldnames_odoo[2]: init_hotel.get_date_scraping(),
                fieldnames_odoo[3]: init_hotel.get_nom_hotel(),
                fieldnames_odoo[4]: init_hotel.get_adr_complete(),
                fieldnames_odoo[5]: init_hotel.get_adresse(),
                fieldnames_odoo[6]: init_hotel.get_ville(),
                fieldnames_odoo[7]: init_hotel.get_code_postal(),
                fieldnames_odoo[8]: init_hotel.get_pays(),
                fieldnames_odoo[9]: init_hotel.get_nombre_etoile(),
                fieldnames_odoo[10]: init_hotel.get_categorie(),
                fieldnames_odoo[11]: init_hotel.get_nb_avis(),
                fieldnames_odoo[12]: init_hotel.get_note_personnel(),
                fieldnames_odoo[13]: init_hotel.get_note_equipements(),
                fieldnames_odoo[14]: init_hotel.get_note_proprete(),
                fieldnames_odoo[15]: init_hotel.get_note_confort(),
                fieldnames_odoo[16]: init_hotel.get_note_qualite_prix(),
                fieldnames_odoo[17]: init_hotel.get_note_emplacement(),
                fieldnames_odoo[18]: init_hotel.get_note_wifi(),
                fieldnames_odoo[19]: init_hotel.get_url_hotel(),
                fieldnames_odoo[20]: init_hotel.get_detail_id_res(),
                fieldnames_odoo[21]: init_hotel.get_id_siren(),
                fieldnames_odoo[22]: init_hotel.get_detail_id_siren(),
                fieldnames_odoo[23]: init_hotel.get_id_valide(),
            }
        )
