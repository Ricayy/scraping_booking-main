# coding=utf8
# Chemin vers le dossier et fichier odoo_backup
from functions.date import get_date_scraping
from path.root_path import root_path

odoo_backup_folder = root_path + "/odoo_backup"
odoo_backup_file = (
    odoo_backup_folder
    + "/odoo_backup_"
    + get_date_scraping()
    + ".txt"
)
