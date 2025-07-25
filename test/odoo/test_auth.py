import unittest

from Class.Odoo import Odoo


class TestAuth(unittest.TestCase):
    def test_auth(self):
        Odoo()
