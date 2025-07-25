# coding=utf8
import os
import xmlrpc.client

from dotenv import load_dotenv

from models.odoo_model import (
    OdooContactModel,
    OdooIdNameModel,
    OdooNoteEtablissementModel,
)
from odoo.odoo_backup import create_odoo_backup

load_dotenv()


def replace_value_with_id(categorie_label, value):
    """
    Fonction de remplacement des valeurs par des identifiants pour la crétion de relations entre les modèles

    Parameters
    ----------
    categorie_label : list[dict]
        Liste des labels
    value : list[dict]
        Liste des valeurs

    Returns
    -------
    data : dict
    """
    data = ""
    for cat_unit in categorie_label:
        # Teste du label à rechercher
        if cat_unit[OdooIdNameModel().x_name] == value:
            # Affectation de l'identifiant correspondant au label
            data = cat_unit["id"]
            # Une fois identifié, on arrête la comparaison
            break
    return data


def replace_value_with_id_note(categorie_note, hotel_note):
    """
    Fonction de remplacement des valeurs par des identifiants pour la création d'une relation avec le modèle des notes

    Parameters
    ----------
    categorie_note : list[dict]
        Liste des labels des notes
    hotel_note : list[dict]
        Liste des valeurs des notes

    Returns
    -------
    data : list[tuple[int, int, dict]]
    """
    data = []
    for hotel_unit in hotel_note:
        for cat_unit in categorie_note:
            # Teste du label de la note à tester
            if (
                cat_unit[OdooIdNameModel().x_name]
                == hotel_unit[2][OdooContactModel().label_note]
            ):
                # Affectation de l'identifiant correspondant au label de la note et des autres valeurs
                data.append(
                    (
                        0,
                        0,
                        {
                            OdooNoteEtablissementModel().date: hotel_unit[2][
                                OdooContactModel().date_note
                            ],
                            OdooNoteEtablissementModel().categorie_note: cat_unit[
                                OdooIdNameModel().id
                            ],
                            OdooNoteEtablissementModel().note: hotel_unit[2][
                                OdooContactModel().valeur_note
                            ],
                        },
                    )
                )
    return data


class Odoo:
    """
    Classe Odoo contenant :
        - Les attributs de connexion à Odoo online
        - Les méthodes de remplacements des valeurs par des identifiants pour la création de relation entre les modèles
        - Les méthodes de publication de création de nouveaux contacts et de modifications des contacts existants

    Attributes
    ----------
    __url_odoo : str
        Url de la bdd
    __db_odoo : str
        Nom de la bdd
    __user_odoo : str
        Nom d'utilisateur
    __pwd_odoo : str
        Mot de passe
    __auth_odoo : _Marshallable
        Instance d'authentification à Odoo online, nécessaire à l'initialisation de modelsOdoo
    __models_odoo : ServerProxy
        Instance de requête à Odoo online, nécessaire pour les requêtes

    __app_contact : str
        Nom technique du modèle des contacts
    __app_pays : str
        Nom technique du modèle des pays
    __app_categorie_etablissement : str
        Nom technique du modèle des catégories des établissements
    __app_classement_etablissement : str
        Nom technique du modèle des classements des établissements
    __app_activite_principale : str
        Nom technique du modèle des activités principales
    __app_activite_registre_metiers : str
        Nom technique du modèle des activités du hotel_data des métiers
    __app_categorie_juridique : str
        Nom technique du modèle des catégories juridiques
    __app_tranche_effectifs_etablissement : str
        Nom technique du modèle des tranches d'effectifs des établissements
    __app_tranche_effectifs_unite_legale : str
        Nom technique du modèle des tranches d'effectifs des unités légales
    __app_categorie_note : str
        Nom technique du modèle des catégories des notes

    Methods
    -------
    __init__ (self) :
        Constructeur de la classe Odoo, qui initialise l'authentification et le modèle des requêtes
    query_search_read_name (self, app_name) :
        Méthode de récupération des identifiants des labels d'un modèle
    normalize_data (self, field_name, hotel_data, app_name) :
        Méthode de récupération des identifiants et labels d'un modèle et de remplacement des valeurs par les identifiants
    prepare_data (self, hotel_data) :
        Méthode de remplacement des valeurs par des identifiants pour créer une relation entre les modèles :
            - catégorie établissement
            - pays
            - classement établissement
            - activité principale
            - activité hotel_data métiers
            - catégorie juridique
            - tranche effectifs établissment
            - tranche effectifs unité légale
            - note établissement
    query_put_odoo (self, id_odoo, hotel_data) :
        Méthode de publication des modifications d'un établissement dans Odoo
    query_search_id (self, url) :
        Méthode de récupération de l'identifiant de la ligne Odoo en fonction de l'url Booking
    query_search_res_name (self, name) :
        Méthode de récupération de l'identifiant de la ligne Odoo en fonction du name res.partner
    """

    __url_odoo = os.getenv("URL_ODOO")
    __db_odoo = os.getenv("DB_ODOO")
    __user_odoo = os.getenv("USER_ODOO")
    __pwd_odoo = os.getenv("PWD_ODOO")
    __auth_odoo = None
    __models_odoo = None

    __app_contact = os.getenv("APP_CONTACT")
    __app_pays = os.getenv("APP_PAYS")
    __app_categorie_etablissement = os.getenv("APP_CATEGORIE_ETABLISSEMENT")
    __app_classement_etablissement = os.getenv("APP_CLASSEMENT_ETABLISSEMENT")
    __app_activite_principale = os.getenv("APP_ACTIVITE_PRINCIPALE")
    __app_activite_registre_metiers = os.getenv("APP_ACTIVITE_REGISTRE_METIERS")
    __app_categorie_juridique = os.getenv("APP_CATEGORIE_JURIDIQUE")
    __app_tranche_effectifs_etablissement = os.getenv(
        "APP_TRANCHE_EFFECTIFS_ETABLISSEMENT"
    )
    __app_tranche_effectifs_unite_legale = os.getenv(
        "APP_TRANCHE_EFFECTIFS_UNITE_LEGALE"
    )
    __app_categorie_note = os.getenv("APP_CATEGORIE_NOTE")

    def __init__(self):
        """
        Constructeur de la classe Odoo, qui initialise l'authentification et le modèle des requêtes
        """
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(self.__url_odoo))
        self.__auth_odoo = common.authenticate(
            self.__db_odoo, self.__user_odoo, self.__pwd_odoo, {}
        )
        self.__models_odoo = xmlrpc.client.ServerProxy(
            "{}/xmlrpc/2/object".format(self.__url_odoo)
        )

    def query_search_read_name(self, app_name):
        """
        Méthode de récupération des identifiants des labels d'un modèle

        Parameters
        ----------
        app_name : str
            Nom du modèle

        Returns
        -------
        [{'id' : '<id1>', 'name' : '<NAME1>'}, {'id' : '<id2>', 'name' : '<NAME2>'}] : list[dict]
        """
        return self.__models_odoo.execute_kw(
            self.__db_odoo,
            self.__auth_odoo,
            self.__pwd_odoo,
            app_name,
            "search_read",
            [],
            {"fields": ["x_name"]},
        )

    def normalize_data(self, field_name, hotel_data, app_name):
        """
        Méthode de récupération des identifiants et labels d'un modèle et normalisation des données

        Parameters
        ----------
        field_name : str
            Nom du champ à normaliser
        hotel_data : dict
            Dictionnaire contenant les données de l'établissement
        app_name : str
            Nom du modèle contenant les identifiants à remplacer
        """
        if field_name in hotel_data:
            # Récupération des identifiants et des labels
            dict_id_value = self.query_search_read_name(app_name)
            # Remplacement de la valeur par l'id
            hotel_data[field_name] = replace_value_with_id(
                dict_id_value, hotel_data[field_name]
            )

    def prepare_data(self, hotel_data):
        """
        Méthode de remplacement des valeurs par des identifiants pour créer une relation entre les modèles :
            - Catégorie établissement
            - Classement établissement
            - Activité principale
            - Activité hotel_data métiers
            - Catégorie juridique
            - Tranche effectifs établissment
            - Tranche effectifs unité légale
            - Pays
            - Note établissement

        Parameters
        ----------
        hotel_data : dict
            Dictionnaire contenant les données d'un établissement
        """
        # Récupération des id des labels pour chacun des modèles en relation
        self.normalize_data(
            OdooContactModel().categorie, hotel_data, self.__app_categorie_etablissement
        )
        self.normalize_data(
            OdooContactModel().classement,
            hotel_data,
            self.__app_classement_etablissement,
        )
        self.normalize_data(
            OdooContactModel().activite_principale,
            hotel_data,
            self.__app_activite_principale,
        )
        self.normalize_data(
            OdooContactModel().activite_registre_metiers,
            hotel_data,
            self.__app_activite_registre_metiers,
        )
        self.normalize_data(
            OdooContactModel().categorie_juridique,
            hotel_data,
            self.__app_categorie_juridique,
        )
        self.normalize_data(
            OdooContactModel().tranche_effectifs_etablissement,
            hotel_data,
            self.__app_tranche_effectifs_etablissement,
        )
        self.normalize_data(
            OdooContactModel().tranche_effectifs_unite_legale,
            hotel_data,
            self.__app_tranche_effectifs_unite_legale,
        )

        # Récupération des id des labels des notes
        if OdooContactModel().note in hotel_data:
            categorie_note = self.query_search_read_name(self.__app_categorie_note)
            # Remplacement de la valeur par l'identifiant
            hotel_data[OdooContactModel().note] = replace_value_with_id_note(
                categorie_note, hotel_data[OdooContactModel().note]
            )

        # Normalisation du nom du pays
        if OdooContactModel().country_id in hotel_data:
            country_id = self.__models_odoo.execute_kw(
                self.__db_odoo,
                self.__auth_odoo,
                self.__pwd_odoo,
                self.__app_pays,
                "search_read",
                [],
                {"fields": ["name"]},
            )
            hotel_data[OdooContactModel().country_id] = replace_value_with_id(
                country_id, hotel_data[OdooContactModel().country_id]
            )

    def query_odoo_post(self, hotel_data):
        """
        Méthode de publication des nouveaux établissements dans Odoo

        Parameters
        ----------
        hotel_data : dict
            Dictionnaire contenant les données à publier sur Odoo
        """
        # Préparation des données au format d'Odoo
        self.prepare_data(hotel_data)
        # Requête de publication du nouvel établissement sur Odoo
        self.__models_odoo.execute_kw(
            self.__db_odoo,
            self.__auth_odoo,
            self.__pwd_odoo,
            self.__app_contact,
            "create",
            [hotel_data],
        )

    def query_odoo_put(self, id_odoo, hotel_data):
        """
        Méthode de publication des modifications d'un établissement dans Odoo

        Parameters
        ----------
        id_odoo : int
            Identifiant Odoo de l'établissement à modifier
        hotel_data : dict
            Dictionnaire contenant les données à publier sur Odoo
        """
        # Préparation des données au format d'Odoo
        self.prepare_data(hotel_data)
        # Requête de publication des modificaitons sur Odoo
        self.__models_odoo.execute_kw(
            self.__db_odoo,
            self.__auth_odoo,
            self.__pwd_odoo,
            self.__app_contact,
            "write",
            [
                [id_odoo],
                hotel_data,
            ],
        )

    def query_search_id(self, url):
        """
        Méthode de récupération de l'identifiant de la ligne Odoo en fonction de l'url Booking

        Parameters
        ----------
        url : str
            Url Booking de l'hôtel à rechercher

        Returns
        -------
        record : list[dict]
        """
        record = self.__models_odoo.execute_kw(
            self.__db_odoo,
            self.__auth_odoo,
            self.__pwd_odoo,
            self.__app_contact,
            "search",
            [[[OdooContactModel().url_booking, "=", url]]],
        )

        return record

    def query_search_res_name(self, name):
        """
        Méthode de récupération de l'identifiant de la ligne Odoo en fonction du name res.partner

        Parameters
        ----------
        name : str
            Nom provenant d'Odoo

        Returns
        -------
        record : list[int] | list[]
        """
        record = self.__models_odoo.execute_kw(
            self.__db_odoo,
            self.__auth_odoo,
            self.__pwd_odoo,
            self.__app_contact,
            "search",
            [[[OdooContactModel().name, "=", name]]],
        )
        if record:
            return record
        else:
            return []

    def test_odoo(self):
        """
        DEBUG

        Fonction de debug test
        """
        try:
            id_odoo = [("id", "=", 67388)]
            record = self.__models_odoo.execute_kw(
                self.__db_odoo,
                self.__auth_odoo,
                self.__pwd_odoo,
                self.__app_contact,
                "write",
                [id_odoo],
                {
                    OdooContactModel().phone: "test",
                },
            )
            print(record)
        except xmlrpc.client.Fault as e:
            print(f"XML-RPC Fault: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def query_odoo_backup(self):
        """
        Méthode de récupération et d'écriture de toutes les lignes d'Odoo dans un fichier texte
        """
        record = []
        # Récupération du nombre de lignes dans Odoo
        count_record = self.__models_odoo.execute_kw(
            self.__db_odoo,
            self.__auth_odoo,
            self.__pwd_odoo,
            self.__app_contact,
            "search_count",
            [[]],
        )
        offset = 0
        # Récupération des lignes de données (1 000 par 1 000)
        for counter in range(1, int(count_record / 1000) + 2):
            # Récupération des id des 1 000 lignes
            ids = self.__models_odoo.execute_kw(
                self.__db_odoo,
                self.__auth_odoo,
                self.__pwd_odoo,
                self.__app_contact,
                "search",
                [[]],
                {"offset": offset, "limit": 1000},
            )
            # Récupération du contenu des lignes
            record = self.__models_odoo.execute_kw(
                self.__db_odoo,
                self.__auth_odoo,
                self.__pwd_odoo,
                self.__app_contact,
                "read",
                [ids],
            )
            # Incrémentation du compteur
            offset = counter * 1000
            # Ecriture des données dans odoo_backup
            create_odoo_backup(record)

    # def split_odoo_post_file(self):
    #     """
    #     Méthodes de segmentation du fichier de publication en CSV de 10 000 lignes et de publication des données sur Odoo
    #     """
    #     # Récupération du chemin vers odoo_post.csv, qui contient les données de scraping
    #     main_csv_file = odoo_post_file
    #     with open(main_csv_file, "r", encoding="utf8") as post_odoo:
    #         reader = csv.DictReader(post_odoo)
    #         count = 0
    #         doc_num = 1
    #         name_file = odoo_post_file.replace(".csv", "_")
    #         name_file += str(doc_num)
    #         name_file += ".csv"
    #         # Lecture des lignes du CSV
    #         for row in reader:
    #             # Initialisation du chemin et name du CSV segmenté
    #             name_file = odoo_post_file.replace(".csv", "_")
    #             name_file += str(doc_num)
    #             name_file += ".csv"
    #             # Pour la première ligne, on initialise l'en-tête
    #             if count == 0:
    #                 count = 1
    #                 # Ecriture de l'en-tête
    #                 with open(
    #                         name_file, "w", encoding="utf8", newline=""
    #                 ) as output_file:
    #                     writer = csv.DictWriter(
    #                         output_file, fieldnames=get_fieldnames_odoo()
    #                     )
    #                     writer.writeheader()
    #             else:
    #                 # Incrémentation du compteur de ligne
    #                 count += 1
    #             # Ecriture de la ligne de données dans odoo_post.csv
    #             with open(name_file, "a", encoding="utf8", newline="") as output_file:
    #                 writer = csv.DictWriter(
    #                     output_file, fieldnames=get_fieldnames_odoo()
    #                 )
    #                 writer.writerow(row)
    #             # Publication du CSV toutes les 10 000 lignes
    #             if count == 10000:
    #                 count = 0
    #                 self.query_odoo_post(name_file)
    #                 doc_num += 1
    #         # Publication des lignes restantes
    #         if name_file != "None":
    #             self.query_odoo_post(name_file)
