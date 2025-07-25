# import os
# import time
# import xmlrpc.client
#
# from dotenv import load_dotenv

import ast
import json
import re

from Class.Odoo import Odoo
from models.odoo_model import OdooContactModel
from odoo.odoo_backup import odoo_backup_file

# from functions.functions_scraping import scraping_booking
# from models.odoo_model import odoo_fields_names, categorie_etablissement_fields, categorie_note_fields, \
#     note_etablissement_fields
#
# load_dotenv()
#
#
# url = os.getenv("URL_ODOO")
# db = os.getenv("DB_ODOO")
# username = os.getenv("USER_ODOO")
# password = os.getenv("PWD_ODOO")
#
# app_contact = os.getenv("APP_CONTACT")
#
# app_categorie_etablissement = os.getenv("APP_CATEGORIE_ETABLISSEMENT")
# app_activite_principale = os.getenv("APP_ACTIVITE_PRINCIPALE")
# app_activite_registre_metiers = os.getenv("APP_ACTIVITE_REGISTRE_METIERS")
# app_categorie_juridique = os.getenv("APP_CATEGORIE_JURIDIQUE")
# app_tranche_effectifs_etablissement = os.getenv("APP_TRANCHE_EFFECTIFS_ETABLISSEMENT")
# app_tranche_effectifs_unite_legale = os.getenv("APP_TRANCHE_EFFECTIFS_UNITE_LEGALE")
# app_categorie_note = os.getenv("APP_CATEGORIE_NOTE")
#
# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# common.version()
# uid = common.authenticate(db, username, password, {})
# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
#
#
# def scrap_and_create_odoo(url_hotel):
#     hotel_data = scraping_booking(url_hotel)
#     print(hotel_data)
#     # prepare_data(hotel_data)
#     # print(hotel_data)
#     # record = models.execute_kw(db, uid, password, app_contact, "create", [hotel_data])
#     # print(record)
#
#
# def replace_value_with_id(categorie_label, value):
#     data = ""
#     for cat_unit in categorie_label:
#         if cat_unit[categorie_etablissement_fields["x_name"]] == value:
#             data = cat_unit["id"]
#             break
#     return data
#
#
# def prepare_note_data(categorie_note, hotel_note):
#     data = []
#     for hotel_unit in hotel_note:
#         for cat_unit in categorie_note:
#             if cat_unit[categorie_note_fields["x_name"]] == hotel_unit[2][odoo_fields_names["label_note"]]:
#                 data.append((0, 0, {
#                     note_etablissement_fields["x_studio_date"]: hotel_unit[2][odoo_fields_names["date_note"]],
#                     note_etablissement_fields["x_studio_catgorie_note"]: cat_unit[categorie_note_fields["id"]],
#                     note_etablissement_fields["x_studio_note"]: hotel_unit[2][odoo_fields_names["valeur_note"]],
#                 }))
#     return data
#
#
# def prepare_data(hotel_data):
#     type_etablissement = models.execute_kw(db, uid, password, app_categorie_etablissement, "search_read", [], {"fields": ["x_name"]})
#     hotel_data[odoo_fields_names["categorie"]] = replace_value_with_id(type_etablissement, hotel_data[odoo_fields_names["categorie"]])
#
#     activite_principale = models.execute_kw(db, uid, password, app_activite_principale, "search_read", [], {"fields": ["x_name"]})
#     hotel_data[odoo_fields_names["activite_principale"]] = replace_value_with_id(activite_principale, hotel_data[odoo_fields_names["activite_principale"]])
#
#     activite_registre_metiers = models.execute_kw(db, uid, password, app_activite_registre_metiers, "search_read", [], {"fields": ["x_name"]})
#     hotel_data[odoo_fields_names["activite_registre_metiers"]] = replace_value_with_id(activite_registre_metiers, hotel_data[odoo_fields_names["activite_registre_metiers"]])
#
#     categorie_juridique = models.execute_kw(db, uid, password, app_categorie_juridique, "search_read", [], {"fields": ["x_name"]})
#     hotel_data[odoo_fields_names["categorie_juridique"]] = replace_value_with_id(categorie_juridique, hotel_data[odoo_fields_names["categorie_juridique"]])
#
#     tranche_effectifs_etablissement = models.execute_kw(db, uid, password, app_tranche_effectifs_etablissement, "search_read", [], {"fields": ["x_name"]})
#     hotel_data[odoo_fields_names["tranche_effectifs_etablissement"]] = replace_value_with_id(tranche_effectifs_etablissement, hotel_data[odoo_fields_names["tranche_effectifs_etablissement"]])
#
#     tranche_effectifs_unite_legale = models.execute_kw(db, uid, password, app_tranche_effectifs_unite_legale, "search_read", [], {"fields": ["x_name"]})
#     hotel_data[odoo_fields_names["tranche_effectifs_unite_legale"]] = replace_value_with_id(tranche_effectifs_unite_legale, hotel_data[odoo_fields_names["tranche_effectifs_unite_legale"]])
#
#     categorie_note = models.execute_kw(db, uid, password, app_categorie_note, 'search_read', [], {'fields': ['x_name']})
#     hotel_data[odoo_fields_names["note"]] = prepare_note_data(categorie_note, hotel_data[odoo_fields_names["note"]])
#
#
# tab_url = [
#     "https://www.booking.com/hotel/fr/alfred-sommier.fr.html",
#     "https://www.booking.com/hotel/fr/solar.fr.html",
#     "https://www.booking.com/hotel/fr/de-l-octroi.fr.html",
#     "https://www.booking.com/hotel/fr/auberge-du-rhone.fr.html",
#     # "https://www.booking.com/hotel/fr/appartement-en-residence-bord-de-mer.fr.html",
#     "https://www.booking.com/hotel/fr/les-gites-du-lavoir-villemoiron-en-othe.fr.html",
#     "https://www.booking.com/hotel/fr/chateaudelile.fr.html",
#     "https://www.booking.com/hotel/fr/restaurant-la-chartreuse.fr.html",
#     "https://www.booking.com/hotel/fr/paris-madrid.fr.html",
#     "https://www.booking.com/hotel/fr/opera-frochot.fr.html",
#     # "https://www.booking.com/hotel/fr/domaine-des-fouques.fr.html",
#     # "https://www.booking.com/hotel/fr/moulin-de-limayrac.fr.html",
# ]
#
# # for url_hotel in tab_url:
# #     print(url_hotel)
# #     scrap_and_create_odoo(url_hotel)
#
# # id_odoo = [('id', '=', 67388)]
# # record = models.execute_kw(db, uid, password, app_contact, "write", [id_odoo], {"website": "nb_avis"})
# # print(record)
#
# Odoo().test_odoo()

test = OdooContactModel()
print(test.name)
