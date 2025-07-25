# Dictionnaire des champs utilisés dans le modèle Contact
from dataclasses import dataclass

odoo_fields_names = {
    # Champs par défaut
    "name": "name",
    "adresse": "street",
    "adresse2": "street2",
    "ville": "city",
    "code_postal": "zip",
    "pays": "country_id",
    "phone": "phone",
    "mobile": "mobile",
    "email": "email",
    "comment": "comment",
    "company_type": "company_type",

    # Champs Booking
    "date_scraping": "x_studio_date_scraping",
    "classement": "x_studio_classement",
    "categorie": "x_studio_categorie_etablissement",
    "nb_avis": "x_studio_nombre_avis",
    "url_booking": "x_studio_url_booking",

    # Champs note
    "note": "x_studio_notes",
    "date_note": "x_studio_date",
    "label_note": "x_studio_type",
    "valeur_note": "x_studio_note",

    # Champs Siren
    "id_siren": "x_studio_identifiant_siren",
    "siret": "x_studio_siret",
    "date_creation": "x_studio_date_de_creation_etablissement",
    "is_entreprise_siege": "x_studio_etablissement_siege",
    "enseigne": "x_studio_enseigne_etablissement",
    "denomination_usuelle": "x_studio_denomination_usuelle_etablissement",
    "activite_principale": "x_studio_activite_principale",
    "activite_registre_metiers": "x_studio_activite_registre_metiers",
    "categorie_juridique": "x_studio_categorie_juridique",
    "tranche_effectifs_etablissement": "x_studio_tranche_effectifs_etablissement",
    "tranche_effectifs_unite_legale": "x_studio_tranche_effectifs_unite_legale",
    "denomination_unite_legale": "x_studio_denomination_unite_legale",
    "nom_unite_legale": "x_studio_nom_unite_legale",
    "nom_usage_unite_legale": "x_studio_nom_usage_unite_legale",
    "prenom_unite_legale": "x_studio_prenom_unite_legale",
    "sexe_unite_legale": "x_studio_sexe_unite_legale",
    "code_cedex": "x_studio_code_cedex",
    "libelle_cedex": "x_studio_libelle_cedex",
}


@dataclass
class OdooContactModel:
    """
    Dataclass contenant les noms des champs du modèle Contacts
    """
    # Champs par défaut
    name = "name"
    street = "street"
    street2 = "street2"
    city = "city"
    zip = "zip"
    country_id = "country_id"
    phone = "phone"
    mobile = "mobile"
    email = "email"
    comment = "comment"
    company_type = "company_type"

    # Champs Booking
    date_scraping = "x_studio_date_scraping"
    classement = "x_studio_classement"
    categorie = "x_studio_categorie_etablissement"
    nb_avis = "x_studio_nombre_avis"
    url_booking = "x_studio_url_booking"

    # Champs notes
    note = "x_studio_notes"
    date_note = "x_studio_date"
    label_note = "x_studio_type"
    valeur_note = "x_studio_note"

    # Champs Siren
    id_siren = "x_studio_identifiant_siren"
    siret = "x_studio_siret"
    date_creation = "x_studio_date_de_creation_etablissement"
    entreprise_siege = "x_studio_etablissement_siege"
    enseigne = "x_studio_enseigne_etablissement"
    denomination_usuelle = "x_studio_denomination_usuelle_etablissement"
    activite_principale = "x_studio_activite_principale"
    activite_registre_metiers = "x_studio_activite_registre_metiers"
    categorie_juridique = "x_studio_categorie_juridique"
    tranche_effectifs_etablissement = "x_studio_tranche_effectifs_etablissement"
    tranche_effectifs_unite_legale = "x_studio_tranche_effectifs_unite_legale"
    denomination_unite_legale = "x_studio_denomination_unite_legale"
    nom_unite_legale = "x_studio_nom_unite_legale"
    nom_usage_unite_legale = "x_studio_nom_usage_unite_legale"
    prenom_unite_legale = "x_studio_prenom_unite_legale"
    sexe_unite_legale = "x_studio_sexe_unite_legale"
    code_cedex = "x_studio_code_cedex"
    libelle_cedex = "x_studio_libelle_cedex"


# Dictionnaire des champs utilisés dans le modèle catégorie établissement
categorie_etablissement_fields = {
    "id": "id",
    "x_name": "x_name",
}


@dataclass
class OdooIdNameModel:
    """
    Dataclass contenant les noms techniques des champs contenant les identifiants et labels à récupérer pour les modèles :
        - Catégorie établissement
        - Activité principale
        - Activité registre métiers
        - Catégorie juridique
        - Tranche effectifs établissement
        - Tranche effectifs unité légale
    """
    id = "id"
    name = "name"
    x_name = "x_name"


# Dictionnaire des champs utilisés dans le modèle activité principale
activite_principale_fields = {
    "id": "id",
    "x_name": "x_name",
}


# Dictionnaire des champs utilisés dans le modèle activité hotel_data métiers
activite_registre_metiers_fields = {
    "id": "id",
    "x_name": "x_name",
}


# Dictionnaire des champs utilisés dans le modèle catégorie juridique
categorie_juridique_fields = {
    "id": "id",
    "x_name": "x_name",
}


# Dictionnaire des champs utilisés dans le modèle tranche effectifs établissement
tranche_effectifs_etablissement_fields = {
    "id": "id",
    "x_name": "x_name",
}


# Dictionnaire des champs utilisés dans le modèle tranche effectifs unité légale
tranche_effectifs_unite_legale_fields = {
    "id": "id",
    "x_name": "x_name",
}


# Dictionnaire des champs utilisés dans le modèle catégorie note
categorie_note_fields = {
    "id": "id",
    "x_name": "x_name",
}


# Dictionnaire des champs utilisés dans le modèle note établissement
note_etablissement_fields = {
    "id": "id",
    "x_studio_date": "x_studio_date",
    "x_studio_categorie_note": "x_studio_type",
    "x_studio_note": "x_studio_note",
}


@dataclass
class OdooNoteEtablissementModel:
    """
    Dataclass contenant les noms techniques des champs du modèle contenant les notes des établissements
    """
    id = "id"
    date = "x_studio_date"
    categorie_note = "x_studio_type"
    note = "x_studio_note"
