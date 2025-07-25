# coding=utf8
from path.odoo_backup import odoo_backup_file


def create_odoo_backup(record):
    """
    Fonction d'écriture des données dans odoo_backup.csv

    Parameters
    ----------
    record : list[]
        Liste des lignes de données contenu dans Odoo
    """
    # Ecriture des données ligne par ligne
    csv_scraping = open(odoo_backup_file, "a", encoding="utf8")
    for row in record:
        csv_scraping.writelines(str(row))
    csv_scraping.close()
