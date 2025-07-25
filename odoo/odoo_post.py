# coding=utf8
import csv

from path.root_path import root_path

# Chemin vers le dossier et fichier odoo_post
odoo_post_folder = root_path + "/odoo_post"
odoo_post_file = odoo_post_folder + "/odoo_post.csv"


def create_post_row_odoo(init_hotel):
    """
    Fonction d'écriture des données de publication dans odoo_post.csv

    Parameters
    ----------
    init_hotel : Hotel
    """
    # Ecriture des lignes de données dans le CSV de publication
    with open(odoo_post_file, "a", encoding="utf8", newline="") as csv_result:
        fieldnames_odoo = get_fieldnames_odoo()
        writer = csv.DictWriter(csv_result, fieldnames=fieldnames_odoo)
        writer.writerow(
            {
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
