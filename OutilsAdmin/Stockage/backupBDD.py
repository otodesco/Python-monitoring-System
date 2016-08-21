#!/usr/bin/env python
# -*- coding: utf-8 -*-



from shutil import copyfile
import datetime
import os
import time

DB_PATH = os.path.dirname(os.path.realpath(__file__))+ '/' + 'adsys.db'
DIRECTORY = os.path.dirname(os.path.realpath(__file__))+ '/' +'backups'
PATTERN_DATE= "%Y-%m-%d %H:%M:%S"

def main(): # L'éxecution en tant que script sauvegarde une copie de la base de donnée
	saveBdd()


def saveBdd():
	"""
	Crée une copie la bdd, puis la copie dans un dossier 
	avec la date de copie comme nom du fichier sauvegardé
	"""
	if not os.path.exists(DIRECTORY):
		os.makedirs(DIRECTORY) # Crée le dossier si non existant
	now = datetime.datetime.now().strftime(PATTERN_DATE)
	copyfile(DB_PATH, DIRECTORY + "/" + now)
	print "Backup crée à la date " + now

def restoreBdd(dateTime=None):
	"""
	Tente de restaurer à une date précise ou alors à la plus récente
	"""
	if dateTime != None:
		strDateTime = dateTime.strftime(PATTERN_DATE)
		if os.path.isfile(DIRECTORY + "/" + strDateTime):
			copyfile(DB_PATH, DIRECTORY + "/" + strDateTime)
			print "La backup " + strDateTime + " a bien été restaurée"
		else :
			print "Erreur : La date recherchée n'a pût être trouvée..."
	else:
		files = sorted(os.listdir(DIRECTORY))
		if len(files) > 0:
			newestBdd = files[-1]
			copyfile(DIRECTORY + "/" + newestBdd, DB_PATH)
			print "La backup " + newestBdd + " a bien été restaurée"
		else:
			print "Erreur : pas de backups trouvées..."




if __name__ == "__main__":
    main()

