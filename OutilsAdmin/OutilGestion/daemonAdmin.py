#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Daemon destiné a être executé par l'administrateur systéme
"""

import logging
import threading
import time
import sys
import subprocess
import signal
from moduleMail import *
from moduleCrise import *

sys.dont_write_bytecode = True


DELAY_CRISIS = 10  # Nombre de secondes entre deux verifications de situation de crise
DELAY_ALERTE = 15 # Nombre de secondes entre deux verifications des alertes du CERT
DELAY_BACKUP_BDD = 5 # Nombre de secondes entre deux sauvegarde de la BDD

class PeriodicThread(object):
    """
    Python periodic Thread using Timer with instant cancellation
    """

    def __init__(self, callback=None, period=1, name=None, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.period = period
        self.stop = False
        self.current_timer = None
        self.schedule_lock = threading.Lock()

    def start(self):
        """
        Mimics Thread standard start method
        """
        self.schedule_timer()

    def run(self):
        """
        By default run callback. Override it if you want to use inheritance
        """
        if self.callback is not None:
            self.callback()

    def _run(self):
        """
        Run desired callback and then reschedule Timer (if thread is not stopped)
        """
        try:
            self.run()
        except Exception, e:
            logging.exception("Exception in running periodic thread")
        finally:
            with self.schedule_lock:
                if not self.stop:
                    self.schedule_timer()

    def schedule_timer(self):
        """
        Schedules next Timer run
        """
        self.current_timer = threading.Timer(self.period, self._run, *self.args, **self.kwargs)
        if self.name:
            self.current_timer.name = self.name
        self.current_timer.start()

    def cancel(self):
        """
        Mimics Timer standard cancel method
        """
        with self.schedule_lock:
            self.stop = True
            if self.current_timer is not None:
                self.current_timer.cancel()

    def join(self):
        """
        Mimics Thread standard join method
        """
        self.current_timer.join()

# END CLASS #


def signal_handler(signal, frame):
	print(' Ctrl+C - Fermeture du programme et des processus appelés')
	timerCrisis.cancel()
	timerAlerte.cancel()
	timerBackupBdd.cancel()
	sys.exit()
signal.signal(signal.SIGINT, signal_handler)



def crisisHandler() :
	print isCrisis()
	if isCrisis() == True :
		print " - Situation de crise detectée, envoi de mail"
		sendMail()

def alerteHandler():
	print (' - Récupération alertes CERT')
	pAlerte = subprocess.Popen("python parseurCERT.py", shell = True) 

def backupBddHandler():
	print (' - Backup BDD')
	pBackupBdd = subprocess.Popen("python ../Stockage/backupBDD.py", shell = True) 
	



####################################
#######          MAIN        #######
####################################

pServ = subprocess.Popen("python ../serveurPython/serveurWeb.py", shell = True) # Ouvre le serveur une fois uniquement

# Création des threads asynchrones
timerCrisis =  PeriodicThread(crisisHandler,DELAY_CRISIS)
timerAlerte =  PeriodicThread(alerteHandler,DELAY_ALERTE)
timerBackupBdd =  PeriodicThread(backupBddHandler,DELAY_BACKUP_BDD)

# Lancement des threads
timerCrisis.start()
timerAlerte.start()
timerBackupBdd.start()


while True:
	time.sleep(1)

