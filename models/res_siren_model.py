# Dictionnaire des champs utilisé dans le fichier res_siren.csv
from dataclasses import dataclass

siren_fields_names = {
    "id_siren": "siren",
    "siret": "siret",
    "date_creation": "dateCreationEtablissement",
    "tranche_effectifs_etablissement": "trancheEffectifsEtablissement",
    "activite_registre_metiers": "activitePrincipaleRegistreMetiersEtablissement",
    "is_entreprise_siege": "etablissementSiege",
    "categorie_juridique": "categorieJuridiqueUniteLegale",
    "denomination_unite_legale": "denominationUniteLegale",
    "sexe_unite_legale": "sexeUniteLegale",
    "nom_unite_legale": "nomUniteLegale",
    "nom_usage_unite_legale": "nomUsageUniteLegale",
    "prenom_unite_legale": "prenomUniteLegale",
    "activite_principale": "activitePrincipaleEtablissement",
    "tranche_effectifs_unite_legale": "trancheEffectifsUniteLegale",
    "adresse2": "complementAdresseEtablissement",
    "adresse": "adresseEtablissement",
    "ville": "libelleCommuneEtablissement",
    "code_postal": "codePostalEtablissement",
    "code_cedex": "codeCedexEtablissement",
    "libelle_cedex": "libelleCedexEtablissement",
    "enseigne": "enseigneEtablissement",
    "denomination_usuelle": "denominationUsuelleEtablissement",
    "email": "email",
    "phone": "phone",
    "mobile": "mobile",
    "comment": "comment",

    "nom_respartner": "nomRespartner",
    "activity_ids": "activity_ids",
    "country_id": "country_id",
    "user_id": "user_id",
    "is_company": "is_company",
    "partner_gid": "partner_gid",
    "company_registry": "company_registry",
    "company_name": "company_name",
    "company_id": "company_id",
    "street2": "street2",
    "industry_id": "industry_id",
    "parent_id": "parent_id",
    "ref_company_ids": "ref_company_ids",
    "category_id": "category_id",
    "company_type": "company_type",
    "phone_mobile_search": "phone_mobile_search",
}


@dataclass
class SirenFieldsModel:
    """
    Dataclass contenant les noms de champs du fichier Siren fusionnés avec res.partner
    """
    # Champs issus de Siren
    id_siren = "siren"
    siret = "siret"
    date_creation = "dateCreationEtablissement"
    tranche_effectifs_etablissement = "trancheEffectifsEtablissement"
    activite_registre_metiers = "activitePrincipaleRegistreMetiersEtablissement"
    is_entreprise_siege = "etablissementSiege"
    categorie_juridique = "categorieJuridiqueUniteLegale"
    denomination_unite_legale = "denominationUniteLegale"
    sexe_unite_legale = "sexeUniteLegale"
    nom_unite_legale = "nomUniteLegale"
    nom_usage_unite_legale = "nomUsageUniteLegale"
    prenom_unite_legale = "prenomUniteLegale"
    activite_principale = "activitePrincipaleEtablissement"
    tranche_effectifs_unite_legale = "trancheEffectifsUniteLegale"
    adresse2 = "complementAdresseEtablissement"
    adresse = "adresseEtablissement"
    ville = "libelleCommuneEtablissement"
    code_postal = "codePostalEtablissement"
    code_cedex = "codeCedexEtablissement"
    libelle_cedex = "libelleCedexEtablissement"
    enseigne = "enseigneEtablissement"
    denomination_usuelle = "denominationUsuelleEtablissement"
    email = "email"
    phone = "phone"
    mobile = "mobile"
    comment = "comment"

    # Champs issus de res.partner
    nom_respartner = "nomRespartner"
    activity_ids = "activity_ids"
    country_id = "country_id"
    user_id = "user_id"
    is_company = "is_company"
    partner_gid = "partner_gid"
    company_registry = "company_registry"
    company_name = "company_name"
    company_id = "company_id"
    street2 = "street2"
    industry_id = "industry_id"
    parent_id = "parent_id"
    ref_company_ids = "ref_company_ids"
    category_id = "category_id"
    company_type = "company_type"
    phone_mobile_search = "phone_mobile_search"
