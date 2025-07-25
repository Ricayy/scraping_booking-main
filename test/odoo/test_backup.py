import unittest

from Class.Odoo import Odoo
from functions.init_project import init_project


class TestBackup(unittest.TestCase):
    def test_backup(self):
        """
        Méthode de test du backup des données d'Odoo
        """
        init_project()
        conn = Odoo()
        conn.query_odoo_backup()
