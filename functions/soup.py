import re

from bs4 import BeautifulSoup
from unidecode import unidecode


def soup_page_booking(page):
    """
    Fonction permettant de récupérer le code source de la page Booking

    Parameters
    ----------
    page : Response
        Résultat de la requête à l'url Booking

    Returns
    -------
    soup_hotel : BeautifulSoup
    """
    # Récupération du code source avec bs4
    soup_hotel = BeautifulSoup(page.content, "html.parser")
    return soup_hotel


def in_soup_nom_hotel(soup_hotel):
    """
    Fonction de récupération du name de l'hôtel dans la page Booking

    Parameters
    ----------
    soup_hotel : BeautifulSoup
        Code source de la page Booking

    Returns
    -------
    nom_hotel : str
    """
    # Récupération du name de l'hôtel
    nom_hotel_soup = soup_hotel.find("a", {"id": "hp_hotel_name_reviews"})
    if nom_hotel_soup:
        nom_hotel = nom_hotel_soup.text.strip()
        return nom_hotel


def in_soup_nombre_etoile(soup_hotel):
    """
    Fonction de récupération du nombre d'étoiles attribué par Booking

    Parameters
    ----------
    soup_hotel : BeautifulSoup
        Code source de la page Booking

    Returns
    -------
    nombre_etoile : str
    """
    # Récupération du classement Booking
    nombre_etoile_soup = soup_hotel.find("span", {"class": "hp__hotel_ratings pp-header__badges pp-header__badges--combined"})
    nombre_etoile_soup = nombre_etoile_soup.find("span")
    if nombre_etoile_soup:
        # Affectation du nombre d'étoiles
        nombre_etoile = len(nombre_etoile_soup.findAll("svg"))
        # Normalisation de l'écriture du classement
        match nombre_etoile:
            case 1:
                nombre_etoile = "1 étoile"
            case 2:
                nombre_etoile = "2 étoiles"
            case 3:
                nombre_etoile = "3 étoiles"
            case 4:
                nombre_etoile = "4 étoiles"
            case 5:
                nombre_etoile = "5 étoiles"
            case 6:
                nombre_etoile = "Palace"
            case _:
                nombre_etoile = "Non classé"
        return nombre_etoile


def in_soup_adr_complete(soup_hotel):
    """
    Fonction de récupération de l'adresse complète de l'hôtel dans la page Booking

    Parameters
    ----------
    soup_hotel : BeautifulSoup
        Code source de la page Booking

    Returns
    -------
    adr_complete : str
    """
    # Récupération de l'adresse complète
    adr_complete_soup = soup_hotel.find("span", {"class": "hp_address_subtitle"})
    if adr_complete_soup is not None:
        # Affectation de l'adresse complète
        adr_complete = adr_complete_soup.text.strip().replace("\n", "")
        return adr_complete


def in_soup_adresse(adr_complete):
    """
    Fonction de récupération de l'adresse de l'hôtel dans la page Booking

    Parameters
    ----------
    adr_complete : str
        Adresse complète sans formatage

    Returns
    -------
    adresse : str
    """
    if adr_complete:
        # Séparation de l'adresse complète par ","
        adr_split = adr_complete.split(",")
        if adr_split:
            adresse = ""
            for i in range(len(adr_split) - 2):
                # Récupération de l'adresse
                adresse += adr_split[i]
            adr_split = adresse.split(" ")
            # Test pour savoir si l'arrondissement est indiqué à la fin de l'adresse
            if "arr" in adr_split[-1] and bool(re.search(r'\d', adr_split[-2])):
                adresse = ""
                # Suppression de l'adresse
                del adr_split[-1]
                del adr_split[-1]
                # Reconstitution de l'adresse
                for word in adr_split:
                    adresse += word + " "
            return adresse.strip()


def in_soup_ville(adr_complete):
    """
    Fonction de récupération de la ville de l'hôtel dans la page Booking

    Parameters
    ----------
    adr_complete : str
        Adresse complète sans formatage

    Returns
    -------
    ville : str
    """
    if adr_complete:
        # Séparation de l'adresse complète par ","
        adr_split = adr_complete.split(",")
        # Séparation dde la ville et du code postal
        cd_ville_split = adr_split[-2].split(" ")
        tab = []
        # Suppression des éléments vides et du code postal
        for i in range(len(cd_ville_split)):
            if (
                cd_ville_split[i] == ""
                or cd_ville_split[i] == " "
                or cd_ville_split[i].isdigit()
            ):
                tab.append(i)
        for i in reversed(tab):
            del cd_ville_split[i]
        if cd_ville_split:
            ville = ""
            # Affectation de la ville mot à mot
            for i in range(len(cd_ville_split)):
                ville += cd_ville_split[i] + " "
            return ville.strip()


def in_soup_code_postal(adr_complete):
    """
    Fonction de récupération du code postal de l'hôtel dans la page Booking

    Parameters
    ----------
    adr_complete : str
        Adresse complète sans formatage

    Returns
    -------
    code_postal : str
    """
    if adr_complete:
        # Séparation de l'adresse complète par ","
        adr_split = adr_complete.split(",")
        # Séparation dde la ville et du code postal
        cd_ville_split = adr_split[-2].split(" ")
        # Suppression des éléments vides
        if cd_ville_split[0] == "" or cd_ville_split[0] == " ":
            del cd_ville_split[0]
        # Affectation du code postal
        if cd_ville_split[0].isdigit():
            code_postal = cd_ville_split[0].strip()
            return code_postal


def in_soup_pays(adr_complete):
    """
    Fonction de récupération du pays de l'hôtel dans la page Booking

    Parameters
    ----------
    adr_complete : str
        Adresse complète sans formatage

    Returns
    -------
    pays : str
    """
    if adr_complete:
        # Séparation de l'adresse complète par ","
        adr_split = adr_complete.split(",")
        # Affectation du pays
        if adr_split:
            pays = adr_split[-1].strip()
            return pays


def in_soup_categorie(soup_hotel):
    """
    Fonction de récupération de la catégorie de l'hôtel dans la page Booking

    Parameters
    ----------
    soup_hotel : BeautifulSoup
        Code source de la page Booking

    Returns
    -------
    categorie : str
    """
    # Récupération du type d'établissement
    categorie_soup = soup_hotel.find("a", {"class": "bui_breadcrumb__link_masked"})
    if categorie_soup is not None:
        categorie_list = categorie_soup.text.replace("\n", "").strip().split(",")
        # Suppression du pays
        if "(France)" in categorie_list[-1]:
            del categorie_list[-1]
        if categorie_list:
            # BRICOLAGE
            # Formatage du type d'établissement
            categorie = categorie_list[-1]
            categorie = categorie.split(" (")
            categorie = categorie[-1]
            if categorie:
                # Formatage et affectation du type d'établissement
                categorie = categorie.replace("(", "").replace(")", "").strip()
                return categorie


def in_soup_nb_avis(soup_hotel):
    """
    Fonction de récupération du nombre d'avis de l'hôtel dans la page Booking

    Parameters
    ----------
    soup_hotel : BeautifulSoup
        Code source de la page Booking

    Returns
    -------
    nb_avis : str
    """
    # Récupération du nombre d'avis Booking
    # nb_avis_soup = soup_hotel.find("div", {"class": "review-score-capla"})
    nb_avis_soup = soup_hotel.find("div", {"data-testid": "review-score-component"})
    if nb_avis_soup:
        nb_avis_soup = nb_avis_soup.findAll("span")
        nb_avis = ""
        for span in nb_avis_soup:
            temp = [int(s) for s in span.text.split() if s.isdigit()]
            temp = str(temp).replace("[", "").replace("]", "").replace(",", "").strip()
            for unit in temp:
                nb_avis += str(unit)
        return int(nb_avis.replace(" ", ""))


def in_soup_note_label(soup_hotel):
    """
    Fonction de récupération des labels et des notes de l'hôtel dans la page Booking

    Parameters
    ----------
    soup_hotel : BeautifulSoup
        Code source de la page Booking

    Returns
    -------
    label : set(str) | None
    """
    label = set()
    # Test de l'existence d'une bar de score
    score_barre_soup = soup_hotel.find("div", {"class": "bui-spacer--larger"})
    if score_barre_soup is not None:
        # Récupération des labels
        label_soup = score_barre_soup.findAll("div", {"data-testid": "review-subscore"})
        if label_soup is not None:
            for span in label_soup:
                label.add(span.text.strip())
        return label
