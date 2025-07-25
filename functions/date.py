# coding=utf8
from datetime import datetime


def get_date_scraping():
    """
    Récupération de la date actuelle

    Returns
    -------
    str (datetime.now().strftime('%Y-%m-%d')) : str
    """
    return str(datetime.now().strftime("%Y-%m-%d"))


def get_date_log():
    """
    Récupération de la date actuelle

    Returns
    -------
    str (datetime.now().strftime('%d-%m-%Y %H:%M:%S')) : str
    """
    return str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))