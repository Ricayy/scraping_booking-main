import unittest

from Class.ScrapingProcessThread import ScrapingProcessThread
from Class.ThreadState import start_thread_queue
from Class.Odoo import Odoo

class MyTestCase(unittest.TestCase):
    def test_init_threading_queue(self):
        thread_id = 1
        tab_url = [
            "https://www.booking.com/hotel/fr/alfred-sommier.fr.html",
            "https://www.booking.com/hotel/fr/solar.fr.html",
            "https://www.booking.com/hotel/fr/de-l-octroi.fr.html",
            "https://www.booking.com/hotel/fr/auberge-du-rhone.fr.html",
            # "https://www.booking.com/hotel/fr/appartement-en-residence-bord-de-mer.fr.html",
            "https://www.booking.com/hotel/fr/les-gites-du-lavoir-villemoiron-en-othe.fr.html",
            "https://www.booking.com/hotel/fr/chateaudelile.fr.html",
            "https://www.booking.com/hotel/fr/restaurant-la-chartreuse.fr.html",
            "https://www.booking.com/hotel/fr/paris-madrid.fr.html",
            "https://www.booking.com/hotel/fr/opera-frochot.fr.html",
            # "https://www.booking.com/hotel/fr/domaine-des-fouques.fr.html",
            # "https://www.booking.com/hotel/fr/moulin-de-limayrac.fr.html",
        ]

        conn = Odoo()

        threads = []
        for url_hotel in tab_url:
            threads.append(ScrapingProcessThread(conn, thread_id, url_hotel))
            thread_id += 1

        start_thread_queue(threads)
