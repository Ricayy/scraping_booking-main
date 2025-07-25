# coding=utf8
import threading
import time

# Tableau de threads en exécution
threads_queue = []


def start_thread_queue(threads):
    """
    Fonction de gestion de la file d'attente des threads

    Parameters
    ----------
    threads :  list[ScrapingProcessThread]
        Tableau contenant l'ensemble des threads initialisés
    """
    check_thread = ThreadState()
    # Démarrage du ThreadPool
    check_thread.start()
    for t in threads:
        while True:
            # Limite de la queue à 24 threads
            if len(threads_queue) <= 24:
                break
        # Démarrage du thread
        t.start()
        # Ajout à la queue de threads
        threads_queue.append(t)
    # Attente de la fin de l'exécution de l'ensemble des threads
    check_thread.join()


class ThreadState(threading.Thread):
    """
    Classe ThreadState contenant :
        - La méthode de gestion des threads terminés

    Methods
    -------
    run (self) :
        Méthode de gestion des threads lors de leurs traitements
    """
    def run(self):
        """
        Méthode de gestion des threads lors de leurs traitements
        """
        while True:
            threads_temp = []
            # Récupération des index des threads terminés
            for i in range(len(threads_queue)):
                if not threads_queue[i].is_alive():
                    threads_temp.append(i)
            # Suppression des threads terminés
            for i in reversed(range(len(threads_temp))):
                del threads_queue[threads_temp[i]]
            # Si la file d'attente est vide pendant cinq secondes alors, on arrête l'execution des threads
            if not threads_queue:
                time.sleep(5)
                if not threads_queue:
                    break
