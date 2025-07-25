import csv
import unittest

from odoo.odoo_backup import odoo_backup_file
from path.root_path import root_path


class MyTestCase(unittest.TestCase):
    def test_count_assoc(self):
        odoo_set = set()
        res_set = set()
        siren_set = set()

        res_list = []
        siren_list = []
        fieldnames = ["id_odoo", "id_res", "id_siren", "count"]
        count_file_name = root_path + "/test/assoc/count.csv"
        with open(count_file_name, "w", encoding="utf8", newline="") as count_file:
            writer = csv.DictWriter(count_file, fieldnames=fieldnames)
            writer.writeheader()

        with open(odoo_backup_file, "r", encoding="utf8") as backup_file:
            backup_reader = csv.DictReader(backup_file)
            for row in backup_reader:
                # Récupération des identifiants
                id_odoo = row["id"]
                res_assoc = row["x_studio_id_respartner"].split(", ")
                siren_assoc = row["x_studio_id_siren"].split(", ")

                # Indexation des identifiants
                odoo_set.add(id_odoo)
                for res_id in res_assoc:
                    res_set.add(res_id)
                    res_list.append(res_id)
                for siren_id in siren_assoc:
                    siren_set.add(siren_id)
                    siren_list.append(siren_id)

        row_count = 1
        for res_id_set in res_set:
            count = 0
            for res_id_list in res_list:
                if res_id_set == res_id_list:
                    count += 1

            with open(count_file_name, "a", encoding="utf8", newline="") as count_file:
                writer = csv.DictWriter(count_file, fieldnames=fieldnames)
                writer.writerow(
                    {
                        fieldnames[0]: row_count,
                        fieldnames[1]: res_id_set,
                        fieldnames[3]: count,
                    }
                )
            row_count += 1

        for siren_id_set in siren_set:
            count = 0
            for siren_id_list in siren_list:
                if siren_id_set == siren_id_list:
                    count += 1

            with open(count_file_name, "a", encoding="utf8", newline="") as count_file:
                writer = csv.DictWriter(count_file, fieldnames=fieldnames)
                writer.writerow(
                    {
                        fieldnames[0]: row_count,
                        fieldnames[2]: siren_id_set,
                        fieldnames[3]: count,
                    }
                )
            row_count += 1
