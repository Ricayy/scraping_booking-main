# coding=utf8
import ast
import csv
import random
import re

import requests
import unidecode

from functions.date import get_date_scraping
from functions.proxies_list import get_proxies_list
from functions.soup import (
    in_soup_adr_complete,
    in_soup_adresse,
    in_soup_categorie,
    in_soup_code_postal,
    in_soup_nb_avis,
    in_soup_nom_hotel,
    in_soup_nombre_etoile,
    in_soup_note_label,
    in_soup_pays,
    in_soup_ville,
    soup_page_booking,
)
from models.odoo_model import OdooContactModel
from models.res_siren_model import SirenFieldsModel
from path.odoo_backup import odoo_backup_file
from path.res_siren import res_siren_file


def requests_url_hotel(url_hotel):
    """
    Fonction de requête des pages Booking à l'aide d'un proxy

    Parameters
    ----------
    url_hotel : str
        Url de la page Booking

    Returns
    -------
    page : Response
    """
    # Déclaration de la liste des proxy disponible
    proxies_list = get_proxies_list()
    # Sélection d'un proxy aléatoire
    proxies = {"http": random.choice(proxies_list)}
    while True:
        # Requête à l'url Booking tant que la page ne renvoi pas un code 200
        page = requests.get(url_hotel, proxies=proxies)
        # Vérification du statut de la page
        if page.status_code == 200:
            break
    return page


def convert_string_to_assoc(string, purge):
    """
    Fonction de formatage des chaines de caractères pour l'association de l'id respartner :
        - Mise en majuscules
        - Suppression des caractères spéciaux
        - Séparation par " "
        - Suppression de l'arrondissement dans l'adresse de la rue
        - Suppression des mots de deux caractères ou moins

    Parameters
    ----------
    string : str
        Chaines de caractères à formatter
    purge : bool
        Booléen pour supprimer les mots faisant moins de deux caractères

    Returns
    -------
    string_ordered : list[str]
    """
    # Formatage de la chaine de caractères (suppression des accents, caractères spéciaux et séparation de la chaine par " "
    string_decode = unidecode.unidecode(string.upper().strip())
    string_cleared = re.sub(r"[^A-Za-z0-9 ]+", " ", string_decode)
    string_split = string_cleared.strip().split(" ")
    if purge:
        # Suppression de l'arrondissement dans la chaine de caractères
        if (
            string_split[len(string_split) - 1] == "ARR"
            or string_split[len(string_split) - 1] == "ARR."
        ):
            del string_split[len(string_split) - 1]
            del string_split[len(string_split) - 1]
        tab = []
        # Récupération index contenant des strings de moins de 2 caractères
        for i in range(len(string_split)):
            if len(string_split[i]) < 3 and not re.search("[0-9]", string_split[i]):
                tab.append(i)
        # Suppression des index
        for i in reversed(tab):
            del string_split[i]
    return string_split


def assoc_scrap_siren(hotel_data):
    """
    Fonction d'association entre les établissements Booking et Siren en comparant :
        - Pays
        - Code postal
        - Ville
        - Adresse

    Parameters
    ----------
    hotel_data : dict
        Modèle de données contenant les informations d'un établissement
    """
    # Déclaration des catégories d'établissement à rechercher dans res_siren
    type_etablissement = [
        "Appart'hôtel",
        "Auberge",
        "Auberge de jeunesse",
        "Bateau-hôtel",
        "Camping",
        "Complexe hôtelier",
        "Hôtel",
        "Lodge",
        "Love hôtel",
        "Maison d'hôtes",
        "Village vacances",
    ]
    for type_unit in type_etablissement:
        if type_unit == hotel_data[OdooContactModel().categorie]:
            # Formatage de l'adresse de l'hôtel scrap, true pour la suppression des mots faisant deux caractères ou moins
            adresse_scrap_ordered = convert_string_to_assoc(
                hotel_data[OdooContactModel().street], True
            )
            # Test de l'existence de l'adresse scrap après formatage
            if adresse_scrap_ordered:
                with open(res_siren_file, "r", encoding="utf8") as res_siren:
                    res_siren_reader = csv.DictReader(res_siren)
                    for row in res_siren_reader:
                        # Test du code postal
                        if (
                            hotel_data[OdooContactModel().zip]
                            == row["codePostalEtablissement"]
                        ):
                            # Formatage du name de la ville
                            ville_scrap_ordered = convert_string_to_assoc(
                                hotel_data[OdooContactModel().city], False
                            )
                            ville_res_siren_ordered = convert_string_to_assoc(
                                row["libelleCommuneEtablissement"], False
                            )
                            # Test du nom de la ville
                            if (
                                ville_scrap_ordered == ville_res_siren_ordered
                                and ville_scrap_ordered
                                and ville_res_siren_ordered
                            ):
                                # Formatage de l'adresse
                                adresse_scrap_ordered = convert_string_to_assoc(
                                    hotel_data[OdooContactModel().street], True
                                )
                                adresse_res_siren_ordered = convert_string_to_assoc(
                                    row["adresseEtablissement"], True
                                )
                                # Test des adresses scrap et siren
                                if adresse_scrap_ordered == adresse_res_siren_ordered:
                                    if (
                                        len(adresse_scrap_ordered) >= 2
                                        and len(adresse_res_siren_ordered) >= 2
                                    ):
                                        # Affectation des données Siren correspondant à l'adresse Booking
                                        hotel_data.update(
                                            {
                                                OdooContactModel().id_siren: row[
                                                    SirenFieldsModel().id_siren
                                                ],
                                                OdooContactModel().siret: row[
                                                    SirenFieldsModel().siret
                                                ],
                                                OdooContactModel().date_creation: row[
                                                    SirenFieldsModel().date_creation
                                                ],
                                                OdooContactModel().tranche_effectifs_etablissement: row[
                                                    SirenFieldsModel().tranche_effectifs_etablissement
                                                ],
                                                OdooContactModel().activite_registre_metiers: row[
                                                    SirenFieldsModel().activite_registre_metiers
                                                ],
                                                OdooContactModel().entreprise_siege: row[
                                                    SirenFieldsModel().is_entreprise_siege
                                                ],
                                                OdooContactModel().categorie_juridique: row[
                                                    SirenFieldsModel().categorie_juridique
                                                ],
                                                OdooContactModel().denomination_unite_legale: row[
                                                    SirenFieldsModel().denomination_unite_legale
                                                ],
                                                OdooContactModel().sexe_unite_legale: row[
                                                    SirenFieldsModel().sexe_unite_legale
                                                ],
                                                OdooContactModel().nom_unite_legale: row[
                                                    SirenFieldsModel().nom_unite_legale
                                                ],
                                                OdooContactModel().nom_usage_unite_legale: row[
                                                    SirenFieldsModel().nom_usage_unite_legale
                                                ],
                                                OdooContactModel().prenom_unite_legale: row[
                                                    SirenFieldsModel().prenom_unite_legale
                                                ],
                                                OdooContactModel().activite_principale: row[
                                                    SirenFieldsModel().activite_principale
                                                ],
                                                OdooContactModel().tranche_effectifs_unite_legale: row[
                                                    SirenFieldsModel().tranche_effectifs_unite_legale
                                                ],
                                                OdooContactModel().street2: row[
                                                    SirenFieldsModel().adresse2
                                                ],
                                                # OdooContactModel().street: row[SirenFieldsModel().street],
                                                # OdooContactModel().city: row[SirenFieldsModel().ville],
                                                # OdooContactModel().zip: row[SirenFieldsModel().code_postal],
                                                OdooContactModel().enseigne: row[
                                                    SirenFieldsModel().enseigne
                                                ],
                                                OdooContactModel().denomination_usuelle: row[
                                                    SirenFieldsModel().denomination_usuelle
                                                ],
                                                OdooContactModel().email: row[
                                                    SirenFieldsModel().email
                                                ],
                                                OdooContactModel().phone: row[
                                                    SirenFieldsModel().phone
                                                ],
                                                OdooContactModel().mobile: row[
                                                    SirenFieldsModel().mobile
                                                ],
                                                OdooContactModel().comment: row[
                                                    SirenFieldsModel().comment
                                                ],
                                                OdooContactModel().code_cedex: row[
                                                    SirenFieldsModel().code_cedex
                                                ],
                                                OdooContactModel().libelle_cedex: row[
                                                    SirenFieldsModel().libelle_cedex
                                                ],
                                            }
                                        )
                                        return row[SirenFieldsModel().nom_respartner]


def scraping_booking(url_hotel):
    """
    Fonction de récupération et d'affectation des données Booking depuis le code source des pages des hôtels

    Parameters
    ----------
    url_hotel : str
        Url Booking de l'hôtel

    Returns
    -------
    hotel_data : dict
        Liste contenant les données de l'établissement
    """
    # Récupération du code source de la page Booking de l'hôtel
    soup_hotel = soup_page_booking(requests_url_hotel(url_hotel))
    hotel_name = in_soup_nom_hotel(soup_hotel)
    # Si le name de l'hôtel n'est pas récupéré alors, on annule le scraping car la page n'éxiste plus
    if hotel_name != "" and hotel_name is not None:
        hotel_data = {
            OdooContactModel().url_booking: url_hotel,
            OdooContactModel().company_type: "company",
            OdooContactModel().name: hotel_name,
        }
        # Test du résultat de l'affectation de l'adresse complète
        full_adress = in_soup_adr_complete(soup_hotel)
        if full_adress != "" and full_adress is not None:
            # Affectation :
            #     - Pays
            #     - Ville
            #     - Code postal
            #     - Adresse
            #     - Date du scraping
            #     - Classement : nombre d'étoiles de l'hôtel
            #     - Catégorie de l'établissement (hôtel, camping, chambres d'hôtes, ...)
            #     - Nombre d'avis publié
            hotel_data.update(
                {
                    OdooContactModel().country_id: in_soup_pays(full_adress),
                    OdooContactModel().city: in_soup_ville(full_adress),
                    OdooContactModel().zip: in_soup_code_postal(full_adress),
                    OdooContactModel().street: in_soup_adresse(full_adress),
                    OdooContactModel().date_scraping: get_date_scraping(),
                    OdooContactModel().classement: in_soup_nombre_etoile(soup_hotel),
                    OdooContactModel().categorie: in_soup_categorie(soup_hotel),
                    OdooContactModel().nb_avis: in_soup_nb_avis(soup_hotel),
                }
            )

            # Récupération du label des notes
            note_data = in_soup_note_label(soup_hotel)
            # Test de l'existence de label
            if note_data:
                note_tab = []
                # Déclaration des labels des notes
                note_label = [
                    "Personnel",
                    "Équipements",
                    "Propreté",
                    "Confort",
                    "Rapport qualité/prix",
                    "Situation géographique",
                    "Connexion Wi-Fi gratuite",
                ]
                for label in note_label:
                    for item in note_data:
                        note = item.split(" ")
                        # Lorsque le label correspond à celui recherché, on attribue la note à ce label
                        if label in item:
                            note_tab.append(
                                (
                                    0,
                                    0,
                                    {
                                        OdooContactModel().date_note: get_date_scraping(),
                                        OdooContactModel().label_note: label,
                                        OdooContactModel().valeur_note: float(
                                            note[-1].replace(",", ".")
                                        ),
                                    },
                                )
                            )
                hotel_data[OdooContactModel().note] = note_tab
            return hotel_data
        return {}


def assoc_scrap_odoo_backup(hotel_data):
    """
    Cherche l'ID Odoo de l'hôtel scrapé dans le fichier odoo_backup

    Parameters
    ----------
    hotel_data : dict
        Dictionnaire contenant les données d'un établissement

    Returns
    -------
    id_odoo : int | False
        L'ID res.partner de la correspondance si trouvée, sinon False
    """
    # Récupération de l'url Booking et de l'adresse de l'établissement
    url_hotel = hotel_data[OdooContactModel().url_booking]
    code_postal_scrap = hotel_data[OdooContactModel().zip]
    ville_scrap = hotel_data[OdooContactModel().city]
    adresse_scrap = hotel_data[OdooContactModel().street]
    with open(odoo_backup_file, "r", encoding="utf8") as backup_file:
        backup_file = backup_file.readlines()
        # Lecture du fichier de backup Odoo
        for line in backup_file:
            # Conversion de la ligne en dictionnaire
            line = line.removeprefix('"').removesuffix('"\n').replace('""', '"')
            infos_odoo = ast.literal_eval(line)
            # Test de l'existence de l'url Booking dans Odoo
            if url_hotel == infos_odoo[OdooContactModel().url_booking]:
                # Retourne l'identifiant Odoo en cas de correspondance
                return int(infos_odoo["id"])
            # Test du code postal
            if code_postal_scrap != infos_odoo[OdooContactModel().zip]:
                continue
            # Normalisation du name de la ville pour la comparaison
            ville_scrap = convert_string_to_assoc(ville_scrap, False)
            ville_siren = convert_string_to_assoc(
                infos_odoo[OdooContactModel().city], False
            )
            if ville_scrap != ville_siren:
                continue
            # Normalisation de l'adresse pour la comparaison
            adresse_scrap = convert_string_to_assoc(adresse_scrap, True)
            adresse_siren = convert_string_to_assoc(
                infos_odoo[OdooContactModel().street], True
            )
            if adresse_scrap != adresse_siren:
                continue
            # Retourne l'identifiant Odoo en cas de correspondance
            return int(infos_odoo["id"])
    # Retourne False dans le cas où une correspondance n'est pas trouvé
    return False
